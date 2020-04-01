from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from .forms import RegisterForm
from django.urls import reverse
from django.contrib import messages
from .models import Identity
from django.contrib.auth.models import User


# Create your views here.
def register(request):
    if request.method == 'POST':
        filledRegisterForm = RegisterForm(request.POST)
        if filledRegisterForm.is_valid():
            filledRegisterForm.save()
            identity = filledRegisterForm.cleaned_data.get('identity')
            # username = filledRegisterForm.cleaned_data.get('username')
            username = filledRegisterForm.cleaned_data.get('username')
            userInstance = User.objects.get(username=username)
            netid = username
            i = Identity(user=userInstance, identity=str(identity), netid=netid)
            i.save()
            return HttpResponseRedirect('/login/')
        else:
            return render(request, 'register/register.html', {'form': filledRegisterForm})
    else:
        registerForm = RegisterForm()
        return render(request, 'register/register.html', {'form': registerForm})
