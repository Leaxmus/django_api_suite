from django.urls import path
from .views import LandingAPI

urlpatterns = [
    path("", LandingAPI.as_view(), name="landing_api_list"),
    path("<str:item_id>/", LandingAPI.as_view(), name="landing_api_detail"),
]