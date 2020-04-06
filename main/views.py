from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from register.models import Identity
from .models import StudentProfile, ProfessorProfile, StudentTags, ProfessorTags
from django.contrib.auth.models import User
from .forms import StudentProfileForm, ProfessorProfileForm, SearchForm
from django.http import JsonResponse
from django.forms.models import model_to_dict
from mongoengine import *


# Create your views here.
def home(request):
    if not request.user.is_anonymous:
        if request.user.is_superuser:
            identity = "superuser"
        else:
            identity = Identity.objects.get(user=request.user).identity
        msg = "Hello, " + str(request.user) + ". You are currently logged in as a " + identity + "."
        # return HttpResponse("Welcome! " + str(request.user) + " as a " + identity)
        sTags = StudentTags(netid='cailiu2', tags=['CV', 'AI'])
        sTags.save()
        pTags = ProfessorTags(netid='abdu', tags=['CV', 'AI'])
        pTags.save()
        # print(1)
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
                               'gpa': studentProfile.gpa, 'department': studentProfile.department})
            else:
                return render(request, 'main/profile.html',
                              {'identity': identity, 'netid': professorProfile.netid, 'name': professorProfile.name,
                               'department': professorProfile.department})


def createProfile(request):
    if request.user.is_anonymous or request.user.is_superuser:
        return render(request, 'main/createProfile.html')

    identity = Identity.objects.get(user=request.user).identity
    netid = Identity.objects.get(user=request.user).netid

    if request.method == 'POST':
        if identity == "student":
            filledProfileForm = StudentProfileForm(request.POST)
            if filledProfileForm.is_valid():
                netid = filledProfileForm.cleaned_data.get('netid')
                name = filledProfileForm.cleaned_data.get('name')
                gpa = filledProfileForm.cleaned_data.get('gpa')
                department = filledProfileForm.cleaned_data.get('department')
                userInstance = User.objects.get(username=request.user.username)
                s = StudentProfile(user=userInstance, netid=netid, name=name, gpa=gpa, department=department)
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
        form = StudentProfileForm(initial={'netid': netid})
    else:
        form = ProfessorProfileForm(initial={'netid': netid})
    msg = "You haven't created a profile yet. Why don't you create it now!"
    return render(request, 'main/createProfile.html', {'form': form, 'msg': msg, 'identity': identity})


def modifyProfile(request):
    if request.user.is_anonymous or request.user.is_superuser:
        return render(request, 'main/modifyProfile.html')

    identity = Identity.objects.get(user=request.user).identity
    netid = Identity.objects.get(user=request.user).netid

    if request.method == 'POST':
        if identity == "student":
            filledProfileForm = StudentProfileForm(request.POST)
            if filledProfileForm.is_valid():
                s = StudentProfile.objects.get(user=request.user)
                s.name = filledProfileForm.cleaned_data.get('name')
                s.gpa = filledProfileForm.cleaned_data.get('gpa')
                s.department = filledProfileForm.cleaned_data.get('department')
                s.save()
                return HttpResponseRedirect('/profile/')
            else:
                return render(request, 'main/modifyProfile.html', {'form': filledProfileForm, 'identity': identity})
        else:
            filledProfileForm = ProfessorProfileForm(request.POST)
            if filledProfileForm.is_valid():
                # userInstance = User.objects.get(username=request.user.username)
                p = ProfessorProfile.objects.get(user=request.user)
                p.name = filledProfileForm.cleaned_data.get('name')
                p.department = filledProfileForm.cleaned_data.get('department')
                p.save()
                return HttpResponseRedirect('/profile/')
            else:
                return render(request, 'main/modifyProfile.html', {'form': filledProfileForm, 'identity': identity})

    if identity == "student":
        s = StudentProfile.objects.get(user=request.user)
        form = StudentProfileForm(initial={'netid': netid, 'name': s.name, 'gpa': s.gpa, 'department': s.department})
    else:
        p = ProfessorProfile.objects.get(user=request.user)
        form = ProfessorProfileForm(initial={'netid': netid, 'name': p.name, 'department': p.department})
    return render(request, 'main/modifyProfile.html', {'form': form, 'identity': identity})


def deleteProfile(request):
    if request.user.is_anonymous or request.user.is_superuser:
        return render(request, 'main/createProfile.html')

    identity = Identity.objects.get(user=request.user).identity
    if identity == "student":
        StudentProfile.objects.filter(user=request.user).delete()
    else:
        ProfessorProfile.objects.filter(user=request.user).delete()

    return redirect('/profile/')




def search(request):
    if request.user.is_anonymous or request.user.is_superuser:
        return render(request, 'main/search.html')
    # print(request)
    identity = Identity.objects.get(user=request.user).identity
    if identity == 'student':
        return render(request, 'main/search.html', {'identity': identity})
    else:
        form = SearchForm()
        if request.is_ajax() and request.method == 'GET':

            # print("Is Ajax!")
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
            data = []
            for sProfile in studentProfiles:
                data.append(model_to_dict(sProfile))
            # print(data)
            return JsonResponse(data, safe=False)
        elif request.method == 'GET':
            studentProfiles = StudentProfile.objects.all()
            nameContain = request.GET.get('nameContain')
            departmentIs = request.GET.get('departmentIs')
            maxGPA = request.GET.get('maxGPA')
            minGPA = request.GET.get('minGPA')
            rawQuery = "SELECT * FROM main_studentprofile WHERE 1=1 "

            if nameContain != '' and nameContain is not None:
                # studentProfiles = studentProfiles.filter(name__icontains=nameContain)
                rawQuery +=  " AND name LIKE '%{nameContain}%'".format(nameContain=nameContain)
            if departmentIs != '' and departmentIs is not None:
                # studentProfiles = studentProfiles.filter(department__exact=departmentIs)
                rawQuery += " AND department = '{departmentIs}'".format(departmentIs=departmentIs)
            if maxGPA != '' and maxGPA is not None:
                # studentProfiles = studentProfiles.filter(gpa__lte=maxGPA)
                rawQuery += " AND GPA <= {maxGPA}".format(maxGPA=maxGPA)
            if minGPA != '' and minGPA is not None:
                rawQuery += " AND GPA >= {minGPA}".format(minGPA=minGPA)
            studentProfiles = studentProfiles.raw(rawQuery)
            form = SearchForm(initial={'nameContain': nameContain, 'departmentIs': departmentIs, 'maxGPA': maxGPA,
                                       'minGPA': minGPA})
            return render(request, 'main/search.html', {'identity': identity, 'form': form, 'results': studentProfiles})

        else:
            return render(request, 'main/search.html', {'identity': identity, 'form': form})
