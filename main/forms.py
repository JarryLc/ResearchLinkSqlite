from django import forms
from django.contrib.auth.models import User

departmentChoices = [
    ('ECE', 'Electrical & Computer Engineering'),
    ('CS', 'Computer Science'),
]

INTEREST_CHOICES = [
    ("Artificial Intelligence", "Artificial Intelligence"),
    ("Computer Architecture", "Computer Architecture"),
    ("Computer Design and Engineering", "Computer Design and Engineering"),
    ("Theoretical Computer Science", "Theoretical Computer Science"),
    ("Information Technology", "Information Technology"),
    ("Operating Systems and Networks", "Operating Systems and Networks"),
    ("Software Applications", "Software Applications"),
    ("Software Engineering", "Software Engineering"),
]

class StudentProfileForm(forms.Form):
    netid = forms.CharField(help_text='Please enter your Illinois NetId.', max_length=20, label='NetId')
    name = forms.CharField(max_length=50)
    gpa = forms.DecimalField(max_digits=3, decimal_places=2, label='GPA')
    department = forms.ChoiceField(choices=departmentChoices)
    interest = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=INTEREST_CHOICES)

class ProfessorProfileForm(forms.Form):
    netid = forms.CharField(help_text='Please enter your Illinois NetId.', max_length=20, label='NetId')
    name = forms.CharField(max_length=50)
    department = forms.ChoiceField(choices=departmentChoices)

class SearchForm(forms.Form):
    nameContain = forms.CharField(help_text="Student's name contains...", max_length=50, label='Name', required=False)
    departmentIs = forms.ChoiceField(choices=departmentChoices, label='Department', required=False)
    maxGPA = forms.DecimalField(max_digits=3, decimal_places=2, label='Maximum GPA', required=False)
    minGPA = forms.DecimalField(max_digits=3, decimal_places=2, label='Minimum GPA', required=False)
