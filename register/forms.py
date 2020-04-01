from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    username = forms.CharField(label="NetId", help_text='Please enter your Illinois NetId.', max_length=20)
    email = forms.EmailField()
    choices = [
        ('student', 'I am a student.'),
        ('professor', 'I am a professor.'),
    ]
    identity = forms.ChoiceField(choices=choices)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "identity"]
