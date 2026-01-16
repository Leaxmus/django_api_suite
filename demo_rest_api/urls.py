from django.urls import path
from .views import DemoRestApi

urlpatterns = [
    path("", DemoRestApi.as_view(), name="demo_rest_api_list"),
    path("<uuid:item_id>/", DemoRestApi.as_view(), name="demo_rest_api_detail"),
]