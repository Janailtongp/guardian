from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from main.models import Client
# Create your views here.


@login_required
def painel(request):
    active_menu: str = "painel"
    title: str = "Painel de controle" 
    subtitle: str = "Descrição da página de painel de controle"
    texto = "Mais informações em: https://zuramai.github.io/mazer/demo/index.html"
    return render(request, "index.html", locals())

@login_required
def clients(request):
    active_menu: str = "clients"
    title: str = "Listagem de empresa" 
    subtitle: str = "Gerencie empresas que poderão ser vinculadas a solicitações"
    clients = Client.objects.all()
    paginator = Paginator(clients, 10)
    page = request.GET.get("page")
    clients_list = paginator.get_page(page)

    return render(request, "clients.html", locals())
