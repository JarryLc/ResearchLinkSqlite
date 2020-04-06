from django.db import models
from django.contrib.auth.models import User
from mongoengine import Document, EmbeddedDocument, fields, DynamicDocument


# Create your models here.


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    netid = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    gpa = models.DecimalField(max_digits=3, decimal_places=2)
    department = models.CharField(max_length=50)


class ProfessorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    netid = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    department = models.CharField(max_length=50)


class StudentTags(DynamicDocument):
    netid = fields.StringField(max_length=20)
    tags = fields.ListField(max_length=100)


class ProfessorTags(DynamicDocument):
    netid = fields.StringField(max_length=20)
    tags = fields.ListField(max_length=100)


class Matches(DynamicDocument):
    netid = fields.StringField(max_length=20)  # Professor's NetId
    candidate = fields.ListField(max_length=100)  # List of candidate's NetId
