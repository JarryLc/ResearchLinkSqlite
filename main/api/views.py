import random
import string

from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
import json
from main.models import StudentProfile, ProfessorProfile, Identity, StudentTags, ProfessorTags, Matches
from .serializers import StudentProfileSerializer, ProfessorProfileSerializer
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
import copy
from django.db import connection
from django.contrib.auth.models import User
import requests

departmentChoicesWithoutEmpty = {'departmentList': ['',
                                                    'Electrical & Computer Engineering',
                                                    'Computer Science',
                                                    'Mechanical Engineering',
                                                    'Chemical Engineering',
                                                    ]}

professorsProfile = [
    # ['A. Alawini', 'alawini@illinois.edu', 'Computer Science', ['Computers and Education', 'Data and Information Systems']],
    # ['A. Bates', 'batesa@illinois.edu', 'Computer Science', ['Operating Systems', 'Security and Privacy']],
    # ['M. Fleck', 'mfleck@illinois.edu', 'Computer Science', ['Artificial Intelligence']],
    # ['Deming Chen', 'dchen@illinois.edu', 'Electrical & Computer Engineering', ['GPU optimization', 'IoT', 'FPGA']],
    # ['Wen-mei Hwu', 'w-hwu@illinois.edu', 'Electrical & Computer Engineering', ['Compilers', 'Cloud computing']],
    # ['Armand Joseph Beaudoin', 'beaudoin@illinois.edu', 'Mechanical Engineering', ['Solid Mechanics and Materials']],
    # ['Pramod Viswanath', 'pramodv@illinois.edu', 'Electrical & Computer Engineering', ['Blockchain', 'Networks']],
    # ['Vikram Adve', 'vadve@illinois.edu', 'Computer Science', ['Architecture', 'Compilers', 'Parallel Computing']],
    # ['Saurabh Gupta', 'saurabhg@illinois.edu', 'Electrical & Computer Engineering', ['Robotics', 'CV']],
    # ['Brian P Bailey', 'bpbailey@illinois.edu', 'Computer Science', ['Interactive Computing']],
    # ['Mattia Gazzola', 'mgazzola@illinois.edu', 'Mechanical Engineering', ['computational soft robotics']],
    # ['M Quinn Brewster', 'brewster@illinois.edu', 'Mechanical Engineering', ['Fluid Mechanics']],
    # ['Paul Fischer', 'fischerp@illinois.edu', 'Computer Science', ['Scientific Computing']],
]
defaultPassword = '123456'


studentTags = ['Computer science', 'Electrical engineering', 'CV', 'ML', 'NLP', 'Database', 'Computer Architecture', 'AI']



RealStudentUser = [
    # ['Sid Kumar', 'sk22', 'sk22@illinois.edu', 3.6, 1, ["ML", "Communication Systems", "Distributed Systems", "Systems", "Computer Architecture"]],
    # ['Gaurav', 'gvs2', 'gvs2@illinois.edu', 3.81, 2, ["ML", "AI"]],
    # ['Sankruth Kota', 'srkota2', 'srkota2@illinois.edu', 3.5, 1, ["ML", "Distributed Systems", "Computer Architecture"]],
    # ['Tak Sum Chan', 'taksumc2', 'taksumc2@illinois.edu', 4.0, 2, ["ML", "Algorithms", "Database"]],
    # ['Josh Perakis', 'perakis2', 'perakis2@illinois.edu', 3.3, 2, ["Cyber security", "Cloud computing"]],
    # ['Jacob Perakis', 'jacobvp2', 'jacobvp2@illinois.edu', 3.63, 2, ["ML", "AI"]],
    # ['Yifan Yang', 'yifany2', 'yifany2@illinois.edu', 3.9, 3, ["Control", "Math"]],
    # ['Tianchi Lu', 'tianchi3', 'tianchi3@illinois.edu', 3.98, 1, ["NLP", "AI"]],
    # ['Shail Desai', 'shailrd2', 'shailrd2@illinois.edu', 2.54, 2, ["ML", "AI", "Big data"]],
    # ['Jiayi Cai', 'jiayic7', 'jiayic7@illinois.edu', 4.0, 1, ["Cloud computing"]],
    # ['Yaxin Peng', 'yaxinp2', 'yaxinp2@illinois.edu', 4.0, 1, ["ML", "Software development"]],
]


def createProfessorUser(request):
    for professor in professorsProfile:
        name = professor[0]
        email = professor[1]
        netid = professor[1].split("@")[0]
        department = professor[2]
        tags = professor[3]
        User.objects.create_user(netid, email, defaultPassword)
        i = Identity(netid=netid, identity='professor')
        i.save()
        p = ProfessorProfile(netid=netid, name=name, department=department)
        p.save()
        t = ProfessorTags(netid=netid, tags=tags)
        t.save()
        print("create for professor " + name)

    return HttpResponse('')


def createStudentUser(request):
    num = 5
    for i in range(num):
        r = requests.get(url='https://randomuser.me/api/')
        data = r.json()
        name = data['results'][0]['name']['first'] + ' ' + data['results'][0]['name']['last']
        email = data['results'][0]['name']['first'].lower() + str(random.randint(2, 10)) + "@illinois.edu"
        netid = data['results'][0]['name']['first'].lower()
        department = departmentChoicesWithoutEmpty['departmentList'][random.randint(1, 3)]
        tags = [studentTags[random.randint(0, len(studentTags) - 1)]]
        gpa = round(float((random.randint(320, 400))/100), 2)
        User.objects.create_user(netid, email, defaultPassword)
        i = Identity(netid=netid, identity='student')
        i.save()
        p = StudentProfile(netid=netid, name=name, gpa=gpa, department=department)
        p.save()
        t = StudentTags(netid=netid, tags=tags)
        t.save()
        print("create for student " + name)
    return HttpResponse('')


def createRealStudentUser(request):
    for s in RealStudentUser:
        name = s[0]
        netid = s[1]
        email = s[2]
        gpa = s[3]
        department = departmentChoicesWithoutEmpty['departmentList'][s[4]]
        tags = s[5]
        User.objects.create_user(netid, email, defaultPassword)
        i = Identity(netid=netid, identity='student')
        i.save()
        p = StudentProfile(netid=netid, name=name, gpa=gpa, department=department)
        p.save()
        t = StudentTags(netid=netid, tags=tags)
        t.save()
        print("create for student " + name)
    return HttpResponse('')




def loginStatus(token):
    t = Token.objects.filter(key__exact=token)
    if len(t) == 0:
        return False, ""
    else:
        return True, t[0].user.username


def getIdentity(netid):
    try:
        id = Identity.objects.get(netid=netid).identity
    except(KeyError, Identity.DoesNotExist):
        return False, ""
    else:
        return True, id


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


# class StudentProfileCreateView(CreateAPIView):
#     queryset = StudentProfile.objects.all()
#     serializer_class = StudentProfileSerializer


def IdentitySignup(request):
    body = json.loads(request.body.decode('utf-8'))
    username = body['username']
    identity = body['identity']
    i = Identity(netid=username, identity=identity)
    i.save()
    responseDict = {'username': username,
                    'identity': identity}
    response = json.dumps(responseDict)
    return JsonResponse(response, safe=False)


def ProfileModifyView(request):
    if request.method == "POST":
        # print(request.body.decode('utf-8'))
        body = json.loads(request.body.decode('utf-8'))
        # print(body)
        netid = body['netid']
        _, identity = getIdentity(netid)
        name = body['name']
        if identity == "student":
            gpa = body['gpa']
        department = body['department']
        tags = body['tags']
        if identity == 'student':
            # update profile in sql database
            rawQuery = "REPLACE into main_studentprofile (netid, name, gpa, department) VALUES('{netid}', '{name}', {gpa}, '{department}')".format(
                netid=netid, name=name, gpa=gpa, department=department)
            with connection.cursor() as cursor:
                cursor.execute(rawQuery)
            # try:
            #     studentProfile = StudentProfile.objects.get(netid=netid)
            # except(KeyError, StudentProfile.DoesNotExist):
            #     s = StudentProfile(netid=netid, name=name, gpa=gpa, department=department)
            #     s.save()
            #     print("add a student profile for " + netid)
            # else:
            #     studentProfile.name = name
            #     studentProfile.gpa = gpa
            #     studentProfile.department = department
            #     studentProfile.save()
            #     print("update a student profile for " + netid)

            # update tags in mongo database
            queryset = StudentTags.objects(netid=netid)
            if len(queryset) == 0:
                t = StudentTags(netid=netid, tags=tags)
                t.save()
                print("add student tags for " + netid)
            else:
                StudentTags.objects(netid=netid).update(tags=tags)
                print("update student tags for " + netid)

        elif identity == "professor":  # Professor
            # update profile in sql database
            rawQuery = "REPLACE into main_professorprofile (netid, name, department) VALUES('{netid}', '{name}', '{department}')".format(
                netid=netid, name=name, department=department)
            with connection.cursor() as cursor:
                cursor.execute(rawQuery)
            # try:
            #     professorProfile = ProfessorProfile.objects.get(netid=netid)
            # except(KeyError, ProfessorProfile.DoesNotExist):
            #     s = ProfessorProfile(netid=netid, name=name, department=department)
            #     s.save()
            #     print("add a professor profile for " + netid)
            # else:
            #     professorProfile.name = name
            #     professorProfile.department = department
            #     professorProfile.save()
            #     print("update a professor profile for " + netid)

            # update tags in mongo database
            queryset = ProfessorTags.objects(netid=netid)
            if len(queryset) == 0:
                t = ProfessorTags(netid=netid, tags=tags)
                t.save()
                print("add professor tags for " + netid)
            else:
                ProfessorTags.objects(netid=netid).update(tags=tags)
                print("update professor tags for " + netid)
        else:
            print("unkonw identity")
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


def GetProfileView(request):
    if request.method == "GET":
        token = request.headers.get('Authorization')
        status, username = loginStatus(token)
        responseDict = {
            "netid": username,
            "name": '',
            "identity": '',
            "gpa": '',
            "department": '',
            "tags": [''],
        }
        if status:
            flag, id = getIdentity(username)
            if flag:
                responseDict["identity"] = id
                if id == "student":
                    try:
                        studentProfile = StudentProfile.objects.get(netid=username)
                    except(KeyError, StudentProfile.DoesNotExist):
                        pass
                    else:
                        responseDict["name"] = studentProfile.name
                        responseDict["gpa"] = float(studentProfile.gpa)
                        responseDict["department"] = studentProfile.department
                    queryset = StudentTags.objects(netid=username)
                    if len(queryset) == 0:
                        tags = ['']
                    else:
                        tags = queryset[0]["tags"]
                    responseDict["tags"] = tags
                else:
                    responseDict["gpa"] = 'N/A'
                    try:
                        professorProfile = ProfessorProfile.objects.get(netid=username)
                    except(KeyError, ProfessorProfile.DoesNotExist):
                        pass
                    else:
                        responseDict["name"] = professorProfile.name
                        responseDict["department"] = professorProfile.department
                    # mongo
                    queryset = ProfessorTags.objects(netid=username)
                    if len(queryset) == 0:
                        tags = ['']
                    else:
                        tags = queryset[0]["tags"]
                    responseDict["tags"] = tags

        print(responseDict)
        response = json.dumps(responseDict)
        return JsonResponse(response, safe=False)


def ProfileDeleteView(request):
    if request.method == "GET":
        token = request.headers.get('Authorization')
        status, username = loginStatus(token)
        if status:
            flag, id = getIdentity(username)
            if flag:
                if id == "student":
                    # sql
                    rawQuery = "DELETE FROM main_studentprofile WHERE netid='{netid}'".format(netid=username)
                    with connection.cursor() as cursor:
                        cursor.execute(rawQuery)
                    # StudentProfile.objects.filter(netid=username).delete()
                    print("delete student profile for " + username)
                    # mongo
                    queryset = StudentTags.objects(netid=username)
                    if len(queryset) == 0:
                        pass
                    else:
                        for i in queryset:
                            i.delete()
                else:
                    # sql
                    rawQuery = "DELETE FROM main_professorprofile WHERE netid='{netid}'".format(netid=username)
                    with connection.cursor() as cursor:
                        cursor.execute(rawQuery)
                    # ProfessorProfile.objects.filter(netid=username).delete()
                    print("delete professor profile for " + username)
                    # mongo
                    queryset = ProfessorTags.objects(netid=username)
                    if len(queryset) == 0:
                        pass
                    else:
                        for i in queryset:
                            i.delete()

        return HttpResponse('')


def StudentProfileSearch(request):
    if request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))
        # print(body)
        nameContain = ''
        departmentIs = ''
        minGPA = ''
        tagContain = ''
        try:
            nameContain = body['nameContain']
        except(KeyError):
            pass
        try:
            departmentIs = body['departmentIs']
        except(KeyError):
            pass
        try:
            minGPA = body['minGPA']
        except(KeyError):
            pass
        try:
            tagContain = body['tagContain']
        except(KeyError):
            pass
        # print(tagContain)
        rawQuery = "SELECT * FROM main_studentprofile WHERE 1=1 "

        # print("search: ", nameContain, departmentIs, minGPA)
        if nameContain != '' and nameContain is not None:
            # studentProfiles = studentProfiles.filter(name__icontains=nameContain)
            rawQuery += " AND name LIKE '%{nameContain}%'".format(nameContain=nameContain)
        if departmentIs != '' and departmentIs is not None:
            # studentProfiles = studentProfiles.filter(department__exact=departmentIs)
            rawQuery += " AND department = '{departmentIs}'".format(departmentIs=departmentIs)
        if minGPA != '' and minGPA is not None:
            rawQuery += " AND GPA >= {minGPA}".format(minGPA=minGPA)
        studentProfiles = StudentProfile.objects.raw(rawQuery)
        # print(studentProfiles)
        responseList = []
        for p in studentProfiles:
            try:
                st = StudentTags.objects(netid=p.netid)
                if tagContain not in st[0]["tags"] and tagContain != '':
                    continue
            except:
                continue
            dic = {
                "netid": p.netid,
                "name": p.name,
                "gpa": float(p.gpa),
                "department": p.department,
            }
            responseList.append(dic)
        # print(type(responseList))
        response = json.dumps(responseList)
        return JsonResponse(response, safe=False)


def ProfessorProfileSearch(request):
    if request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))
        # print(body)
        nameContain = ''
        departmentIs = ''
        tagContain = ''
        try:
            nameContain = body['nameContain']
        except(KeyError):
            pass
        try:
            departmentIs = body['departmentIs']
        except(KeyError):
            pass
        try:
            tagContain = body['tagContain']
        except(KeyError):
            pass
        rawQuery = "SELECT * FROM main_professorprofile WHERE 1=1 "
        print("search: ", nameContain, departmentIs)
        if nameContain != '' and nameContain is not None:
            # studentProfiles = studentProfiles.filter(name__icontains=nameContain)
            rawQuery += " AND name LIKE '%{nameContain}%'".format(nameContain=nameContain)
        if departmentIs != '' and departmentIs is not None:
            # studentProfiles = studentProfiles.filter(department__exact=departmentIs)
            rawQuery += " AND department = '{departmentIs}'".format(departmentIs=departmentIs)
        professorProfiles = ProfessorProfile.objects.raw(rawQuery)
        # print(studentProfiles)
        responseList = []
        for p in professorProfiles:
            try:
                pt = ProfessorTags.objects(netid=p.netid)
                if tagContain not in pt[0]["tags"] and tagContain != '':
                    continue
            except:
                continue
            dic = {
                "netid": p.netid,
                "name": p.name,
                "department": p.department,
            }
            responseList.append(dic)
        # print(type(responseList))
        response = json.dumps(responseList)
        return JsonResponse(response, safe=False)


def recommendation():
    with connection.cursor() as cursor:
        cursor.execute("SELECT department, AVG(gpa) FROM main_studentprofile GROUP BY department")
        row = cursor.fetchone()
        stat = {}
        while row:
            department = row[0]
            avg = row[1]
            stat[department] = round(avg, 3)
            row = cursor.fetchone()



    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT * FROM main_studentprofile AS s JOIN main_professorprofile AS p ON s.department=p.department")
        matches = {}
        row = cursor.fetchone()
        while row:
            # print(row)
            student = row[0]
            gpa = row[2]
            department = row[3]
            professor = row[4]

            if gpa < stat[department]:
                print(student, "gpa is lower than average")
                row = cursor.fetchone()
                continue

            if student not in matches.keys():
                matches[student] = [professor]
            else:
                if professor not in matches[student]:
                    matches[student].append(professor)

            if professor not in matches.keys():
                matches[professor] = [student]
            else:
                if student not in matches[professor]:
                    matches[professor].append(student)
            row = cursor.fetchone()
        for netid in matches:
            queryset = Matches.objects(netid=netid)
            if len(queryset) == 0:
                m = Matches(netid=netid, candidate=matches[netid])
                m.save()
                print("add matches for " + netid)
            else:
                Matches.objects(netid=netid).update(candidate=matches[netid])
                print("update matches for " + netid)


def RecommendationView(request):
    recommendation()
    token = request.headers.get('Authorization')
    status, username = loginStatus(token)
    if request.method == "GET":
        response = []
        queryset = Matches.objects(netid=username)
        print(queryset)
        if len(queryset) > 0:
            list = queryset[0].candidate
            for candidate in list:
                subDict = {}
                subDict['netid'] = candidate
                email = User.objects.get(username=candidate).email
                subDict['email'] = email
                response.append(subDict)
        response = json.dumps(response)
        return JsonResponse(response, safe=False)


def statistics(request):
    if request.method == "GET":
        with connection.cursor() as cursor:
            cursor.execute("SELECT department, AVG(gpa) FROM main_studentprofile GROUP BY department")
            row = cursor.fetchone()
            stat = []
            while row:
                subDict = {}
                department = row[0]
                avg = row[1]
                subDict['department'] = department
                subDict['avg'] = round(avg, 3)
                stat.append(subDict)
                row = cursor.fetchone()
            response = json.dumps(stat)
            return JsonResponse(response, safe=False)
