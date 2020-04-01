from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('profile/create/', views.createProfile, name='createProfile'),
    path('profile/modify/', views.modifyProfile, name='modifyProfile'),
    path('profile/delete/', views.deleteProfile, name='deleteProfile'),

    path('search/', views.search, name='search'),
]