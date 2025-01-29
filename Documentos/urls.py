from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_documentos, name='listar_documentos'),
    path('criar/', views.criar_documento, name='criar_documento'),
    path('editar/<int:documento_id>/', views.editar_documento, name='editar_documento'),
    path('excluir/<int:documento_id>/', views.excluir_documento, name='excluir_documento'),
    path('detalhes/<int:documento_id>/', views.detalhes_documento, name='detalhes_documento'),
    path('conceder_permissao/', views.conceder_permissao, name='conceder_permissao'),
    path('permissoes/', views.visualizar_permissoes, name='visualizar_permissoes'),
    path('permissoes/excluir/<int:permissao_id>/', views.excluir_permissao, name='excluir_permissao'),
    path('arquivo/<int:documento_id>/', views.servir_arquivo_protegido, name='servir_arquivo_protegido'),
]
