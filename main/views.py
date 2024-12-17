from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from main.models import Client, User
from .forms import ClientForm
from dal import autocomplete
# Create your views here.


class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = User.objects.filter(is_staff=False, is_active=True)
        if self.q:
            qs = qs.filter(name=self.q)
        return qs

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
    clients = Client.objects.all().order_by("legal_name")
    paginator = Paginator(clients, 10)
    page = request.GET.get("page")
    clients_list = paginator.get_page(page)

    return render(request, "clients-list.html", locals())

@login_required
def create_client(request):
    active_menu: str = "clients"
    title: str = "Cadastro de empresa"
    subtitle: str = "Formulário de cadastro de empresa" 
    if request.method == "POST":
        form = ClientForm(request.POST)

        if form.is_valid():
            client = form.save(commit=False)
            client.save()
            collaborators = form.cleaned_data['collaborators']
            client.collaborators.add(*collaborators)
            
            return redirect("/clients/")
    else:
        form = ClientForm()
    return render(request, "clients-new.html", locals())


@login_required
def edit_client(request, id):
    active_menu: str = "clients"
    title: str = "Edição de empresa"
    subtitle: str = "Formulário de edição de empresa"

    client = get_object_or_404(Client, pk=id)
    form = ClientForm(instance=client)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save(commit=False)
            client.save()
            collaborators = form.cleaned_data['collaborators']
            client.collaborators.clear()
            client.collaborators.add(*collaborators)
            return redirect("/clients/")
        else:
            return render(request, "clients-edit.html", locals())
    else:
        return render(request, "clients-edit.html", locals())


@login_required
def delete_client(request, id):
    active_menu: str = "clients"
    title: str = ""
    subtitle: str = ""

    client = get_object_or_404(Client, pk=id)
    client.delete()
    messages.info(request, "Cliente deletado com sucesso!")
    return redirect("/clients/")
