from django.db import models
from django.contrib.auth.models import User


class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.IntegerField(max_length=15)
    date_of_birth = models.DateField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Car(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    inventory_count = models.IntegerField()
    sales_count = models.IntegerField()

    def __str__(self):
        return self.model