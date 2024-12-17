from django.conf import settings
from django.urls import path
from main import views
urlpatterns = [
    path('user-autocomplete', views.UserAutocomplete.as_view(), name="user-autocomplete"),
    
    path("", views.painel),
    path("clients/", views.clients),
    path("clients/new/", views.create_client),
    path("clients/<int:id>/edit", views.edit_client),
    path("clients/<int:id>/delete", views.delete_client),
]