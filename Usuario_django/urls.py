from django.urls import path
from . import views

urlpatterns = [
    path("cadastro/",views.cadastro, name='cadastro'),
    path("login/",views.login, name='login'),
    path("logout/",views.logout, name='logout'),
    path("esqueceu_senha/",views.esqueceu_senha, name='esqueceu_senha'),
    path("alterar_senha/",views.alterar_senha, name='alterar_senha'),
    path("listar_usuarios/",views.listar_usuarios, name='listar_usuarios'),
    path('excluir_usuario/<int:usuario_id>/', views.excluir_usuario, name='excluir_usuario'),
]
