from django.urls import path
from .views import LandingAPI

urlpatterns = [
    path("", LandingAPI.as_view(), name="index"),
]
