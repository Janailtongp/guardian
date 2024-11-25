from django.conf import settings
from django.urls import path

from main import views

urlpatterns = [
    path(
        "painel/",
        views.painel,
    ),
]