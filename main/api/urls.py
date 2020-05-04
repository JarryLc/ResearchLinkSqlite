from django.urls import path
from .views import (StudentProfileListView,
                    ProfessorProfileListView,
                    StudentTagsListView,
                    ProfessorTagsListView,
                    MatchesListView,
                    ProfileModifyView,
                    DepartmentListView,
                    GetUsernameView,
                    IdentitySignup,
                    GetProfileView,
                    ProfileDeleteView,
                    StudentProfileSearch,
                    ProfessorProfileSearch,
                    statistics,
                    RecommendationView,
                    createProfessorUser,
                    createStudentUser,
                    createRealStudentUser)
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('StudentProfileList/', StudentProfileListView.as_view(), name='StudentProfileListView'),
    path('ProfessorProfileList/', ProfessorProfileListView.as_view(), name='ProfessorProfileListView'),

    path('StudentTagsList/', StudentTagsListView.as_view(), name='StudentTagsListView'),
    path('ProfessorTagsList/', ProfessorTagsListView.as_view(), name='ProfessorTagsListView'),
    path('MatchesList/', MatchesListView.as_view(), name='MatchesListView'),
    # path('<pk>', IdentityDetailView.as_view(), name='IdentityDetailView'),


    path('StudentProfileList/search/', csrf_exempt(StudentProfileSearch)),
    path('ProfessorProfileList/search/', csrf_exempt(ProfessorProfileSearch)),


    path('profile/modify/', csrf_exempt(ProfileModifyView)),
    path('profile/delete/', ProfileDeleteView),

    path('identitySignup/', csrf_exempt(IdentitySignup)),

    path('departmentList/', DepartmentListView),
    path('getUsername/', GetUsernameView),
    path('getProfile/', GetProfileView),
    path('statistics/', statistics),
    path('recommendation/', RecommendationView),

    path('support/professor/', createProfessorUser),
    path('support/randomStudent/', createStudentUser),
    path('support/realStudent/', createRealStudentUser),

]