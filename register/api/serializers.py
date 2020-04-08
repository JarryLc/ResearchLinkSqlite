from rest_framework import serializers
from register.models import Identity


class IdentitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Identity
        fields = ('user', 'netid', 'identity')