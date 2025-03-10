from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, Http404,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import *
from Usuario_django.models import Usuario
from autenticacao import * 
import os


@is_user
def listar_documentos(request):
    # Lista os documentos do usuário logado
    documentos_proprios = Documento.objects.filter(proprietario=request.user.usuario).order_by("-data_documento")
    documentos_por_tipo = {}
    for doc in documentos_proprios:
        tipo = doc.tipo.tipo
        if tipo not in documentos_por_tipo:
            documentos_por_tipo[tipo] = []
        documentos_por_tipo[tipo].append(doc)
    # Lista os documentos que o usuário pode ver devido a permissões recebidas

    permissoes = PermissaoDocumento.objects.filter(usuario_permitido=request.user.usuario)
    documentos_compartilhados = Documento.objects.filter(proprietario__in=permissoes.values('usuario_concedente'),secreto=False).order_by("proprietario",'-data_documento')
    documentos_compartilhados_usuario={}
    for doc in documentos_compartilhados:
        if doc.proprietario.usuario not in documentos_compartilhados_usuario:
            documentos_compartilhados_usuario[doc.proprietario.usuario]={}
        tipo = doc.tipo.tipo
        if tipo not in documentos_compartilhados_usuario[doc.proprietario.usuario]:
            documentos_compartilhados_usuario[doc.proprietario.usuario][tipo] = []
        documentos_compartilhados_usuario[doc.proprietario.usuario][tipo].append(doc)    
    print(documentos_compartilhados_usuario)
    return render(request, 'listar.html', {
        'documentos_proprios': documentos_por_tipo,
        'documentos_compartilhados': documentos_compartilhados_usuario,
    })


@is_user
def criar_documento(request):
    tipos = Tipo_documento.objects.all().order_by("tipo")
    if request.method == 'POST':
        titulo=request.POST.get('titulo')
        resumo = request.POST.get('resumo')
        arquivo= request.FILES.get("arquivo")
        data=request.POST.get("data_documento")
        secreto=(request.POST.get("secreto")=="on")
        tipo_id = request.POST.get("tipo") 
        tipo = Tipo_documento.objects.filter(id=tipo_id).first()
        if arquivo:
            tamanho_maximo = 5 * 1024 * 1024  # 5 MB em bytes
            if arquivo.size > tamanho_maximo:
                messages.error(request, 'O arquivo não pode ser maior que 5 MB.')
                return render(request, 'criar.html', {"tipos": tipos})
                
        documento = Documento(proprietario=request.user.usuario,titulo=titulo,secreto=secreto,
                              resumo=resumo, arquivo=arquivo,data_documento=data,tipo=tipo)
        documento.save()
        messages.success(request, 'Documento criado com sucesso!')
        return redirect('listar_documentos')
    
    return render(request, 'criar.html', {"tipos":tipos})


@is_user
def editar_documento(request, documento_id):
    tipos = Tipo_documento.objects.all().order_by("tipo")
    documento = get_object_or_404(Documento, id=documento_id)
    if not documento.pode_editar(request.user.usuario):
        messages.error(request, 'Você não tem permissão para editar este documento.')
        return redirect('listar_documentos')

    if request.method == 'POST':
        titulo=request.POST.get('titulo')
        resumo = request.POST.get('resumo')
        arquivo= request.FILES.get("arquivo")        
        data=request.POST.get("data_documento")
        secreto=(request.POST.get("secreto")=="on")
        tipo_id = request.POST.get("tipo") 
        tipo = Tipo_documento.objects.filter(id=tipo_id).first()
        documento = get_object_or_404(Documento, id=documento_id)
        documento.titulo=titulo
        documento.resumo=resumo
        documento.tipo=tipo
        if arquivo:
            tamanho_maximo = 5 * 1024 * 1024  # 5 MB em bytes
            if arquivo.size > tamanho_maximo:
                messages.error(request, 'O arquivo não pode ser maior que 5 MB.')
                return render(request, 'editar.html', {'documento': documento,"tipos":tipos})
            caminho_arquivo=os.path.join(settings.PROTECTED_MEDIA_ROOT,'media', str(documento.arquivo))
            try:
                if documento.arquivo:
                    os.remove(caminho_arquivo)
                documento.arquivo = arquivo
            except:
                messages.error(request, 'O arquivo não pode ser Apagado do servidor, consulte o administrador.')
                return redirect('listar_documentos')
        documento.data_documento=data
        documento.secreto=secreto
        documento.save()
        messages.success(request, 'Documento atualizado com sucesso!')
        return redirect('listar_documentos')
    return render(request, 'editar.html', {'documento': documento,"tipos":tipos})

@is_user
def detalhes_documento(request, documento_id):
    documento = get_object_or_404(Documento, id=documento_id)

    if not documento.pode_visualizar(request.user.usuario):
        messages.error(request, 'Você não tem permissão para visualizar este documento.')
        return redirect('listar_documentos')

    return render(request, 'detalhes.html', {'documento': documento})

@is_user
def excluir_documento(request, documento_id):
    documento = get_object_or_404(Documento, id=documento_id)
    if not documento.pode_excluir(request.user.usuario):
        messages.error(request, 'Você não tem permissão para excluir este documento.')
        return redirect('listar_documentos')
    
    try:
        caminho_arquivo = os.path.join(settings.PROTECTED_MEDIA_ROOT,'media', str(documento.arquivo))
        if documento.arquivo:
            os.remove(caminho_arquivo)
        documento.delete() 
        messages.success(request, 'Documento excluído com sucesso!')
        return redirect('listar_documentos')
    except Exception as e:
        messages.error(request, f'Erro ao excluir documento - {e}<br>{caminho_arquivo} - - {documento.arquivo}')

    return redirect('listar_documentos')


@is_user
def conceder_permissao(request):
    if request.method == 'POST':
        cpf_usuario = ''.join(filter(str.isdigit, request.POST.get("cpf_usuario")))
        print(cpf_usuario, Usuario.objects.filter(cpf=cpf_usuario))
        print(cpf_usuario, Usuario.objects.all())
        try:
            usuario_permitido = Usuario.objects.get(cpf=cpf_usuario)
            # Verifica se a permissão já existe
            if not PermissaoDocumento.objects.filter(usuario_concedente=request.user.usuario, usuario_permitido=usuario_permitido).exists():
                PermissaoDocumento.objects.create(usuario_concedente=request.user.usuario, usuario_permitido=usuario_permitido)
                messages.success(request, f'Permissão concedida a {usuario_permitido.cpf}.')
            else:
                messages.warning(request, f'{usuario_permitido.cpf} já tem permissão para ver seus documentos.')
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')
        return redirect('listar_documentos')

    return render(request, 'conceder_permissao.html')



@is_user
def visualizar_permissoes(request):
    # Lista todas as permissões concedidas pelo usuário logado
    permissoes_concedidas = PermissaoDocumento.objects.filter(usuario_concedente=request.user.usuario)
    return render(request, 'visualizar_permissoes.html', {
        'permissoes_concedidas': permissoes_concedidas,
    })

@is_user
def excluir_permissao(request, permissao_id):
    permissao = get_object_or_404(PermissaoDocumento, id=permissao_id)

    # Verifica se o usuário logado é o concedente da permissão
    if permissao.usuario_concedente != request.user.usuario:
        messages.error(request, 'Você não tem permissão para revogar esta permissão.')
        return redirect('visualizar_permissoes')

    # Exclui a permissão
    permissao.delete()
    messages.success(request, 'Permissão revogada com sucesso!')
    return redirect('visualizar_permissoes')

@is_user
def servir_arquivo_protegido(request, documento_id):
    # Obtém o documento
    documento = Documento.objects.filter(id=documento_id).first()
    # print(documento,documento.arquivo)
    if not documento:
        raise Http404("Documento não encontrado.")

    # Verifica se o usuário tem permissão para visualizar
    if not documento.pode_visualizar(request.user.usuario):
        raise Http404("Você não tem permissão para acessar este arquivo.")

    # Caminho absoluto do arquivo
    caminho_arquivo = os.path.join(settings.PROTECTED_MEDIA_ROOT,'media', str(documento.arquivo))
    # print(caminho_arquivo)
    
    if not os.path.exists(caminho_arquivo):
        raise Http404("Arquivo não encontrado.")
    
    # Servir o arquivo como resposta
    with open(caminho_arquivo, "rb") as arquivo:
        figuras = ["jpg", "jpeg", "bmp", "gif", "svg", "png"]
        ext = str(documento.arquivo).split(".")[-1].lower()
        
        if ext in figuras:
            content_type = f'image/{ext if ext != "jpg" else "jpeg"}'  # Exceção para 'jpg' que deve ser 'jpeg'
            response = HttpResponse(arquivo.read(), content_type=content_type)
        else:
            response = HttpResponse(
                arquivo.read(), content_type="application/octet-stream"
            )
            filename = str(documento.arquivo).split("/")[-1]
            response["Content-Disposition"] = f'attachment; filename="{filename}"'

    return response
    
    
    return FileResponse(open(caminho_arquivo, 'rb'), as_attachment=True, filename=documento.arquivo.name)
@is_admin
def cadastrar_especialidade(request):
    if request.method == 'POST':
        tipo_cadastrado=request.POST.get('especialidade')
        
        tipo = Tipo_documento(tipo=tipo_cadastrado)
        tipo.save()
        messages.success(request, 'Documento criado com sucesso!')
        return redirect('home')
    else:
        return render(request, 'criar_tipos.html')
@is_admin
def listar_especialidades(request):
    # Lista os documentos do usuário logado
    tipos = Tipo_documento.objects.all()
    return render(request, 'listar_tipos.html', {
        "tipos":tipos
    })
@is_admin
def excluir_especialidades(request,id_tipo):
    tipo=get_object_or_404(Tipo_documento,id=id_tipo)
    # Exclui a permissão
    documentos=Documento.objects.filter(tipo=tipo)
    if documentos:
        messages.error(request,"Especilidade não pode ser excluida pois está em uso!")
        return redirect('listar_especialidades')
    tipo.delete()
    messages.success(request, 'Especialidade excluida com sucesso!')
    return redirect('listar_especialidades')