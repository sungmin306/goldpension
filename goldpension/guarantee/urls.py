from django.urls import path,include
from .views import GcompanyView
from rest_framework.routers import DefaultRouter



urlpatterns = [
    path('company/',GcompanyView.as_view())
]