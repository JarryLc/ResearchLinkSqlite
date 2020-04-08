from rest_framework import serializers
from main.models import StudentProfile, ProfessorProfile


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ('user', 'netid', 'name', 'gpa', 'department')


class ProfessorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessorProfile
        fields = ('user', 'netid', 'name', 'department')

