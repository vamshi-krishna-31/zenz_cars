import pandas as pd
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .forms import UploadFileForm, UserRegistrationForm, LoginForm
from .models import Car
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required(login_url='/')
def dashboard(request):
    selected_year = request.GET.get('year')
    if selected_year:
        cars = Car.objects.filter(year=selected_year)
    else:
        cars = Car.objects.all()

    # Get distinct years from the Car model
    years = Car.objects.values_list('year', flat=True).distinct()

    return render(request, 'dashboard.html', {'cars': cars, 'years': years, 'selected_year': selected_year})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    return redirect('login')


@login_required(login_url='/')
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            file_path = fs.path(filename)
            data = pd.read_excel(file_path)
            # Process the uploaded file and save data to the database
            for index, row in data.iterrows():
                Car.objects.create(
                    make=row['Make'],
                    model=row['Model'],
                    year=row['Year'],
                    inventory_count=row['Inventory Count'],
                    sales_count=row['Sales Count']
                )
            return redirect('dashboard')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
