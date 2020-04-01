from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import StudentProfile
from .models import ProfessorProfile
from register.models import Identity

departmentChoices = [
    ('ECE', 'Electrical & Computer Engineering'),
    ('CS', 'Computer Science'),
]

departmentChoicesWithEmpty = [
    ('', ''),
    ('ECE', 'Electrical & Computer Engineering'),
    ('CS', 'Computer Science'),
]


class StudentProfileForm(forms.Form):
    netid = forms.CharField(max_length=20, label='NetId', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    name = forms.CharField(max_length=50, help_text='Only professors can see your name.')
    gpa = forms.DecimalField(max_digits=3, decimal_places=2, label='GPA')
    department = forms.ChoiceField(choices=departmentChoices)


class ProfessorProfileForm(forms.Form):
    netid = forms.CharField(max_length=20, label='NetId', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    name = forms.CharField(max_length=50)
    department = forms.ChoiceField(choices=departmentChoices)


class SearchForm(forms.Form):
    nameContain = forms.CharField(help_text="Student's name contains...", max_length=50, label='Name', required=False)
    departmentIs = forms.ChoiceField(choices=departmentChoicesWithEmpty, label='Department', required=False)
    maxGPA = forms.DecimalField(max_digits=3, decimal_places=2, label='Maximum GPA', required=False)
    minGPA = forms.DecimalField(max_digits=3, decimal_places=2, label='Minimum GPA', required=False)
