from rest_framework.generics import ListAPIView, RetrieveAPIView
from register.models import Identity
from .serializers import IdentitySerializer


class IdentityListView(ListAPIView):
    queryset = Identity.objects.all()
    serializer_class = IdentitySerializer


class IdentityDetailView(RetrieveAPIView):
    queryset = Identity.objects.all()
    serializer_class = IdentitySerializer
