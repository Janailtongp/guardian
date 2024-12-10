from django import forms
from .models import Client, User
from django.contrib.admin.widgets import FilteredSelectMultiple
from dal import autocomplete


class ClientForm(autocomplete.FutureModelForm):
    collaborators = forms.ModelMultipleChoiceField(
        label='Colaboradores', 
        queryset=User.objects.all(), 
        widget=autocomplete.ModelSelect2Multiple(url='user-autocomplete')
    )
    class Meta:
        model = Client
        fields = ("legal_name", "cnpj", "cpf", "collaborators")

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'