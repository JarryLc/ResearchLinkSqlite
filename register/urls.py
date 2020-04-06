from django.contrib import admin
from django.urls import include, path
from . import views
from main import views as v

urlpatterns = [
    path('', views.register, name='register'),
]
