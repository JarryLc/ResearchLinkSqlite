from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from register.models import Identity


# Create your views here.
def home(request):

    if not request.user.is_anonymous:
        identity = Identity.objects.get(user=request.user).identity
        return HttpResponse("Welcome! " + str(request.user) + " as a " + identity)
    else:
        return HttpResponse("Welcome! " + str(request.user))
