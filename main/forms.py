from django import forms
from .models import Client, User, RoutineType
from django.contrib.admin.widgets import FilteredSelectMultiple
from dal import autocomplete


class ClientForm(autocomplete.FutureModelForm):
    collaborators = forms.ModelMultipleChoiceField(
        label='Colaboradores', 
        queryset=User.objects.all(), 
        widget=autocomplete.ModelSelect2Multiple(url='user-autocomplete'),
        required=False,
        help_text="Colaboradores possuem acesso a processos da empresa",
    )
    class Meta:
        model = Client
        fields = ("legal_name", "cnpj", "cpf", "collaborators")

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class RoutineTypeForm(autocomplete.FutureModelForm):
    class Meta:
        model = RoutineType
        fields = ("code", "name", "description")

    def __init__(self, *args, **kwargs):
        super(RoutineTypeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'