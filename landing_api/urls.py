from django.urls import path
from .views import LandingAPI, landing_api_interface

urlpatterns = [
    path("", landing_api_interface, name="landing_api_interface"),
    path("api/", LandingAPI.as_view(), name="landing_api_list"),
    path("api/<str:item_id>/", LandingAPI.as_view(), name="landing_api_detail"),
]