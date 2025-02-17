from django.urls import path
from .views import get_random_setup

urlpatterns = [
    path("random_setup/", get_random_setup, name="random_setup"),
]
