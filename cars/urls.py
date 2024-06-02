from django.urls import path
from .views import register, dashboard, upload_file, login_view, logout_view

urlpatterns = [
    path('', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('upload/', upload_file, name='upload'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]