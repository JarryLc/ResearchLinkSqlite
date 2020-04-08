from django.urls import path
from .views import (StudentProfileListView,
                    ProfessorProfileListView,
                    StudentTagsListView,
                    ProfessorTagsListView,
                    MatchesListView,
                    StudentCreateView)
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('StudentProfileList/', StudentProfileListView.as_view(), name='StudentProfileListView'),
    path('ProfessorProfileList/', ProfessorProfileListView.as_view(), name='ProfessorProfileListView'),
    path('StudentTagsList/', StudentTagsListView.as_view(), name='StudentTagsListView'),
    path('ProfessorTagsList/', ProfessorTagsListView.as_view(), name='ProfessorTagsListView'),
    path('MatchesList/', MatchesListView.as_view(), name='MatchesListView'),
    # path('<pk>', IdentityDetailView.as_view(), name='IdentityDetailView'),

    path('StudentProfile/create/', csrf_exempt(StudentCreateView)),
]