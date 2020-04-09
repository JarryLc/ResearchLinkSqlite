from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from register.models import Identity
from .models import StudentProfile
from .models import ProfessorProfile
from django.contrib.auth.models import User
from .forms import StudentProfileForm, ProfessorProfileForm, SearchForm
from newsapi import NewsApiClient
import random
from random import shuffle
# Create your views here.
def home(request):
    newsapi = NewsApiClient(api_key="463f3a16242547968dbe75909735ddf4")
    topheadlines = newsapi.get_top_headlines(category='technology', language= 'en', country = 'us')
    sources = newsapi.get_sources()
    mySrc = sources['sources']


    articles = topheadlines['articles']
    desc = []
    news = []
    img = []
    href = []
    tit = []
    for i in range(len(articles)):
        myarticles = articles[i]
        srcIter = mySrc[i]
        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
        href.append(myarticles['url'])
        tit.append(srcIter['name'])
        seed = random.randint(2,len(articles)-3)
    mylist = zip(news, desc, img, href)

    if not request.user.is_anonymous:
        if request.user.is_superuser:
            identity = "superuser"
        else:
            identity = Identity.objects.get(user=request.user).identity
        msg = "Hello, " + str(request.user) + ". You are currently logged in as a " + identity + "."
        # return HttpResponse("Welcome! " + str(request.user) + " as a " + identity)
        return render(request, 'main/home.html', {'msg': msg, 'identity': identity, 'n1':tit[0+seed],
        'n2':tit[1+seed], 'n3':tit[2+seed],'h1':href[0+seed], 'h2':href[1+seed], 'h3':href[2+seed],
        'd1':desc[0+seed], 'd2':desc[1+seed], 'd3':desc[2+seed],
        'img1':img[0+seed], 'img2':img[1+seed], 'img3':img[2+seed]})
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

def about(request):
    return render(request, 'main/about.html')

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
