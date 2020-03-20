from django import forms
from django.contrib.auth.models import User

departmentChoices = [
    ('ECE', 'Electrical & Computer Engineering'),
    ('CS', 'Computer Science'),
]


class StudentProfileForm(forms.Form):
    netid = forms.CharField(help_text='Please enter your Illinois NetId.', max_length=20, label='NetId')
    name = forms.CharField(max_length=50)
    gpa = forms.DecimalField(max_digits=3, decimal_places=2, label='GPA')
    department = forms.ChoiceField(choices=departmentChoices)


class ProfessorProfileForm(forms.Form):
    netid = forms.CharField(help_text='Please enter your Illinois NetId.', max_length=20, label='NetId')
    name = forms.CharField(max_length=50)
    department = forms.ChoiceField(choices=departmentChoices)
