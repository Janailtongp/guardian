from django.shortcuts import render
from main.models import Client
# Create your views here.


def painel(request):
    active_menu: str = "painel"
    title: str = "Painel de controle" 
    subtitle: str = "Descrição da página de painel de controle"
    texto = "Mais informações em: https://zuramai.github.io/mazer/demo/index.html"
    return render(request, "index.html", locals())

def clients(request):
    active_menu: str = "clients"
    title: str = "Listagem de empresa" 
    subtitle: str = "Gerencie empresas que poderão ser vinculadas a solicitações"
    clients = Client.objects.all()
    return render(request, "clients.html", locals())
