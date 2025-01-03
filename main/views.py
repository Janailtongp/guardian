from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from main.models import Client, User, RoutineType, Routine
from .forms import ClientForm, RoutineTypeForm
from dal import autocomplete
# Create your views here.


class UserAutocomplete(autocomplete.Select2QuerySetView):
    def get_result_label(self, item):
        return f"{item.name} (@{item.username})"

    def get_selected_result_label(self, item):
        return f"{item.name} (@{item.username})"

    def get_queryset(self):
        qs = User.objects.filter(is_staff=False, is_active=True)
        if self.q:
            qs = qs.filter(Q(name__icontains=self.q) | Q(username__icontains=self.q))
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
    title: str = "Empresas" 
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



@login_required
def routinetypes(request):
    active_menu: str = "routinetypes"
    title: str = "Tipos de Solicitações" 
    subtitle: str = "Gerencie os Tipos Solicitações"
    routinetypes = RoutineType.objects.all().order_by("code")
    paginator = Paginator(routinetypes, 10)
    page = request.GET.get("page")
    routinetypes_list = paginator.get_page(page)

    return render(request, "routinetypes-list.html", locals())

@login_required
def create_routinetype(request):
    active_menu: str = "routinetypes"
    title: str = "Tipos de Solicitações"
    subtitle: str = "Formulário de cadastro de Tipo de Solicitação" 
    if request.method == "POST":
        form = RoutineTypeForm(request.POST)

        if form.is_valid():
            routinetype = form.save(commit=False)
            routinetype.save()
    
            return redirect("/routinetypes/")
    else:
        form = RoutineTypeForm()
    return render(request, "routinetypes-new.html", locals())


@login_required
def edit_routinetype(request, id):
    active_menu: str = "routinetypes"
    title: str = "Tipos de Solicitações"
    subtitle: str = "Formulário de edição de Tipo de Solicitação"

    client = get_object_or_404(RoutineType, pk=id)
    form = RoutineTypeForm(instance=client)

    if request.method == 'POST':
        form = RoutineTypeForm(request.POST, instance=client)
        if form.is_valid():
            client = form.save(commit=False)
            client.save()

            return redirect("/routinetypes/")
        else:
            return render(request, "routinetypes-edit.html", locals())
    else:
        return render(request, "routinetypes-edit.html", locals())


@login_required
def delete_routinetype(request, id):
    active_menu: str = "routinetypes"
    title: str = ""
    subtitle: str = ""

    routinetype = get_object_or_404(RoutineType, pk=id)
    routinetype.delete()
    messages.info(request, "Tipo de serviço deletado com sucesso!")
    return redirect("/routinetypes/")