from django.conf import settings
from django.urls import path

from main import views

urlpatterns = [
    path("", views.painel),
    path("clients/", views.clients),
]