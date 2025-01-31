from django.urls import path
from . import views

urlpatterns = [
    path("cadastro/",views.cadastro, name='cadastro'),
    path("login/",views.login, name='login'),
    path("logout/",views.logout, name='logout'),
    path("esqueceu_senha/",views.esqueceu_senha, name='esqueceu_senha'),
    path("alterar_senha/",views.alterar_senha, name='alterar_senha'),
]
