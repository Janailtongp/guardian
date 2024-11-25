from django.shortcuts import render

# Create your views here.


def painel(request):
    title: str = "Painel de controle" 
    subtitle: str = "Descrição da página de painel de controle"
    texto = "Mais informações em: https://zuramai.github.io/mazer/demo/index.html"
    return render(request, "index.html", locals())
