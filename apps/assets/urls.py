from django.urls import path

from . import views

urlpatterns = [
    path("", views.assets, name="assets"),
    path("assets/config", views.configuration, name="configuration")
]