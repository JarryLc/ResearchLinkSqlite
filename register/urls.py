from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('react/', views.react, name='react'),
]