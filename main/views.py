from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from register.models import Identity
from .models import StudentProfile
from .models import ProfessorProfile
from django.contrib.auth.models import User
from .forms import StudentProfileForm, ProfessorProfileForm, SearchForm


# Create your views here.
def home(request):
    if not request.user.is_anonymous:
        if request.user.is_superuser:
            identity = "superuser"
        else:
            identity = Identity.objects.get(user=request.user).identity
        msg = "Hello, " + str(request.user) + ". You are currently logged in as a " + identity + "."
        # return HttpResponse("Welcome! " + str(request.user) + " as a " + identity)
        return render(request, 'main/home.html', {'msg': msg, 'identity': identity})
    else:
        msg = "You are not logged in currently."
        return render(request, 'main/home.html', {'msg': msg})
        # return HttpResponse("Welcome! " + str(request.user))


def profile(request):
    if request.user.is_anonymous or request.user.is_superuser:
        return render(request, 'main/profile.html')
    else:
        identity = Identity.objects.get(user=request.user).identity
        try:
            if identity == "student":
                studentProfile = StudentProfile.objects.get(user=request.user)
            else:
                professorProfile = ProfessorProfile.objects.get(user=request.user)
        except(KeyError, StudentProfile.DoesNotExist):
            return redirect('/profile/create/')
        except(KeyError, ProfessorProfile.DoesNotExist):
            return redirect('/profile/create/')
        else:
            if identity == "student":
                return render(request, 'main/profile.html',
                              {'identity': identity, 'netid': studentProfile.netid, 'name': studentProfile.name,
                               'gpa': studentProfile.gpa, 'department': studentProfile.department, 'interest': studentProfile.interest})
            else:
                return render(request, 'main/profile.html',
                              {'identity': identity, 'netid': professorProfile.netid, 'name': professorProfile.name,
                               'department': professorProfile.department})


def createProfile(request):
    if request.user.is_anonymous or request.user.is_superuser:
        return render(request, 'main/createProfile.html')

    identity = Identity.objects.get(user=request.user).identity

    if request.method == 'POST':
        if identity == "student":
            filledProfileForm = StudentProfileForm(request.POST)
            if filledProfileForm.is_valid():
                netid = filledProfileForm.cleaned_data.get('netid')
                name = filledProfileForm.cleaned_data.get('name')
                gpa = filledProfileForm.cleaned_data.get('gpa')
                department = filledProfileForm.cleaned_data.get('department')
                interest = filledProfileForm.cleaned_data.get('interest')
                userInstance = User.objects.get(username=request.user.username)
                s = StudentProfile(user=userInstance, netid=netid, name=name, gpa=gpa, department=department, interest=interest)
                s.save()
                return HttpResponseRedirect('/profile/')
            else:
                return render(request, 'main/createProfile.html', {'form': filledProfileForm, 'identity': identity})
        else:
            filledProfileForm = ProfessorProfileForm(request.POST)
            if filledProfileForm.is_valid():
                netid = filledProfileForm.cleaned_data.get('netid')
                name = filledProfileForm.cleaned_data.get('name')
                department = filledProfileForm.cleaned_data.get('department')
                userInstance = User.objects.get(username=request.user.username)
                p = ProfessorProfile(user=userInstance, netid=netid, name=name, department=department)
                p.save()
                return HttpResponseRedirect('/profile/')
            else:
                return render(request, 'main/createProfile.html', {'form': filledProfileForm, 'identity': identity})

    if identity == "student":
        form = StudentProfileForm()
    else:
        form = ProfessorProfileForm()
    msg = "You haven't created a profile yet. Why don't you create it now!"
    return render(request, 'main/createProfile.html', {'form': form, 'msg': msg, 'identity': identity})


def modifyProfile(request):
    if request.user.is_anonymous or request.user.is_superuser:
        return render(request, 'main/modifyProfile.html')

    identity = Identity.objects.get(user=request.user).identity

    if request.method == 'POST':
        if identity == "student":
            filledProfileForm = StudentProfileForm(request.POST)
            if filledProfileForm.is_valid():
                userInstance = User.objects.get(username=request.user.username)
                s = StudentProfile.objects.get(user=userInstance)
                s.netid = filledProfileForm.cleaned_data.get('netid')
                s.name = filledProfileForm.cleaned_data.get('name')
                s.gpa = filledProfileForm.cleaned_data.get('gpa')
                s.department = filledProfileForm.cleaned_data.get('department')
                s.interest = filledProfileForm.cleaned_data.get('interest')
                s.save()
                return HttpResponseRedirect('/profile/')
            else:
                return render(request, 'main/modifyProfile.html', {'form': filledProfileForm, 'identity': identity})
        else:
            filledProfileForm = ProfessorProfileForm(request.POST)
            if filledProfileForm.is_valid():
                userInstance = User.objects.get(username=request.user.username)
                p = ProfessorProfile.objects.get(user=userInstance)
                p.netid = filledProfileForm.cleaned_data.get('netid')
                p.name = filledProfileForm.cleaned_data.get('name')
                p.department = filledProfileForm.cleaned_data.get('department')
                p.save()
                return HttpResponseRedirect('/profile/')
            else:
                return render(request, 'main/modifyProfile.html', {'form': filledProfileForm, 'identity': identity})

    if identity == "student":
        form = StudentProfileForm()
    else:
        form = ProfessorProfileForm()
    return render(request, 'main/modifyProfile.html', {'form': form, 'identity': identity})


def search(request):
    if request.user.is_anonymous or request.user.is_superuser:
        return render(request, 'main/search.html')

    identity = Identity.objects.get(user=request.user).identity
    if identity == 'student':
        return render(request, 'main/search.html', {'identity': identity})
    else:
        form = SearchForm()
        if request.method == 'GET':
            studentProfiles = StudentProfile.objects.all()
            nameContain = request.GET.get('nameContain')
            departmentIs = request.GET.get('departmentIs')
            maxGPA = request.GET.get('maxGPA')
            minGPA = request.GET.get('minGPA')
            if nameContain != '' and nameContain is not None:
                studentProfiles = studentProfiles.filter(name__icontains=nameContain)
            if departmentIs != '' and departmentIs is not None:
                studentProfiles = studentProfiles.filter(department__exact=departmentIs)
            if maxGPA != '' and maxGPA is not None:
                studentProfiles = studentProfiles.filter(gpa__lte=maxGPA)
            if minGPA != '' and minGPA is not None:
                studentProfiles = studentProfiles.filter(gpa__gte=minGPA)


            return render(request, 'main/search.html', {'identity': identity, 'form': form, 'results': studentProfiles})
        else:
            return render(request, 'main/search.html', {'identity': identity, 'form': form})
