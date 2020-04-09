from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
import json
from main.models import StudentProfile, ProfessorProfile, StudentTags, ProfessorTags, Matches
from .serializers import StudentProfileSerializer, ProfessorProfileSerializer
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
import copy

departmentChoicesWithoutEmpty = {'departmentList': ['Electrical & Computer Engineering',
                                                    'Computer Science',
                                                    ]}


def loginStatus(token):
    t = Token.objects.filter(key__exact=token)
    if len(t) == 0:
        return False, ""
    else:
        return True, t[0].user.username


class StudentProfileListView(ListAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer


class ProfessorProfileListView(ListAPIView):
    queryset = ProfessorProfile.objects.all()
    serializer_class = ProfessorProfileSerializer


class StudentTagsListView(View):
    def get(self, request):
        querysetJson = StudentTags.objects.all().to_json()
        return JsonResponse(querysetJson, safe=False)

    def post(self, request):
        pass


class ProfessorTagsListView(View):
    def get(self, request):
        querysetJson = ProfessorTags.objects.all().to_json()
        return JsonResponse(querysetJson, safe=False)

    def post(self, request):
        pass


class MatchesListView(View):
    def get(self, request):
        querysetJson = Matches.objects.all().to_json()
        return JsonResponse(querysetJson, safe=False)

    def post(self, request):
        pass


# class IdentityDetailView(RetrieveAPIView):
#     queryset = Identity.objects.all()
#     serializer_class = IdentitySerializer


class StudentProfileCreateView(CreateAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer


def StudentCreateView(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            print("yes")
            print(request.user)
        else:
            print(request.user)
        # print(request.body.decode('utf-8'))
        body = json.loads(request.body.decode('utf-8'))
        print(body)
        netid = body['netid']
        name = body['name']
        gpa = body['gpa']
        department = body['department']
        tags = body['tags']
        print(netid, name, gpa, department, tags)
        s = StudentTags.objects(netid=netid).update(tags=tags)

        return HttpResponse(1)


def DepartmentListView(request):
    token = request.headers.get('Authorization')
    status, username = loginStatus(token)
    if request.method == "GET":
        responseDict = copy.deepcopy(departmentChoicesWithoutEmpty)
        responseDict['username'] = username
        response = json.dumps(responseDict)
        return JsonResponse(response, safe=False)


def GetUsernameView(request):
    if request.method == "GET":
        token = request.headers.get('Authorization')
        status, username = loginStatus(token)
        username = {"username": username}
        response = json.dumps(username)
        return JsonResponse(response, safe=False)
