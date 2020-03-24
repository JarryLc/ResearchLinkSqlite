from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    netid = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    gpa = models.DecimalField(max_digits=3, decimal_places=2)
    department = models.CharField(max_length=50)
    interest = models.CharField(max_length=50)

class ProfessorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    netid = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
