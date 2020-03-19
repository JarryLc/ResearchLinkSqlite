from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from register.models import Identity


# Create your views here.
def home(request):
    if not request.user.is_anonymous:
        if request.user.is_superuser:
            identity = "superuser"
        else:
            identity = Identity.objects.get(user=request.user).identity
        msg = "Hello, " + str(request.user) + ". You are currently logged in as a " + identity + "."
        # return HttpResponse("Welcome! " + str(request.user) + " as a " + identity)
        return render(request, 'main/home.html', {'msg': msg})
    else:
        msg = "You are not logged in currently."
        return render(request, 'main/home.html', {'msg': msg})
        # return HttpResponse("Welcome! " + str(request.user))
