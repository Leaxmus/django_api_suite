from django.urls import path
from .views import DemoRestApi, demo_api_interface

urlpatterns = [
    path("", demo_api_interface, name="demo_api_interface"),
    path("api/", DemoRestApi.as_view(), name="demo_rest_api_list"),
    path("api/<uuid:item_id>/", DemoRestApi.as_view(), name="demo_rest_api_detail"),
]