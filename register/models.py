from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Identity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    netid = models.CharField(max_length=20)
    identity = models.CharField(max_length=100)
