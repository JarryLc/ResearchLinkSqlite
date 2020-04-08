from django.urls import path
from .views import IdentityListView, IdentityDetailView


urlpatterns = [
    path('', IdentityListView.as_view(), name='IdentityListView'),
    path('<pk>', IdentityDetailView.as_view(), name='IdentityDetailView'),
]