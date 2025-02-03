from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from hashlib import sha256
from .models import *
from autenticacao import *
from auxiliares import *


@is_user
def logout(request):
    django_logout(request)
    return redirect("login")

@is_user
def home(request):
    return render(request,"home.html")

@is_user
def alterar_senha(request):
    if request.method=="GET":
        return render(request,"alterar_senha.html")
    elif request.method=="POST":
       usuario_logado=request.user
       cpf=Usuario.objects.filter(usuario=usuario_logado).first().cpf
       senha_atual=request.POST.get("senha_atual")
       senha_nova1=request.POST.get("senha_nova1")
       senha_nova2=request.POST.get("senha_nova2")
       if senha_nova1==senha_nova2:
           user = authenticate(request, username=cpf, password=senha_atual) 
           print(user)
           if user is not None:
            user.set_password(senha_nova1)
            user.save()
            django_logout(request)
            return redirect("login")
       else:
           messages.warning(request,"Senha não são iguais, tente novamente!")
           return render(request,"alterar_senha.html") 
       messages.warning(request,"Senha atual incorreta, tente novamente")
       return render(request,"alterar_senha.html")   
    
@is_admin
def listar_usuarios(request):
    if request.method=="GET":
        usuarios=Usuario.objects.all()
        return render(request,"listar_usuarios.html",{'usuarios':usuarios})
    messages.error(request, 'Erro ao acessar lista de usuários')
    return render(request,"login.html")
@is_admin
def excluir_usuario(request,usuario_id):
    messages.error(request, 'Função não implementada')
    usuarios=Usuario.objects.all()
    return render(request,"listar_usuarios.html",{'usuarios':usuarios})

def login(request):
    if request.method=="GET":
        return render(request,"login.html")
    elif request.method=="POST":
        cpf = ''.join(filter(str.isdigit, request.POST.get("cpf")))
        password = request.POST["senha"]
        user = authenticate(request, username=cpf, password=password)
        if user is not None:
            django_login(request, user)
            return render(request,"home.html")
    messages.error(request, 'Usuario ou senha não conferem')
    return redirect("login")

def cadastro(request):
    
    is_admin_user = request.user.is_authenticated and is_user(request.user)
    lista_tipos_usuarios={}

    
    if request.method=="GET":
  
        if is_admin_user: 
            lista_tipos_usuarios={"tipos":list(Tipo_usuario.objects.all())}
        else:
            lista_tipos_usuarios={"tipos":[]}
        lista_tipos_usuarios['is_admin_user']=is_admin_user    
        return render(request,"cadastro.html",lista_tipos_usuarios)
        
    elif request.method=='POST':   
        email=request.POST.get("email")
        first_name= request.POST.get("first_name")
        last_name= request.POST.get("last_name")
        senha=request.POST.get("senha")
        cpf = ''.join(filter(str.isdigit, request.POST.get("cpf")))
        if not validar_cpf(cpf):
            if is_admin_user:
                return render(request, "cadastro.html", {
                    "tipos": list(Tipo_usuario.objects.all()),'is_admin_user':is_admin_user,
                    "erro": "CPF inválido. Por favor, insira um CPF válido."})
            else:
                 return render(request, "cadastro.html", {
                    "tipos": [],'is_admin_user':is_admin_user,
                    "erro": "CPF inválido. Por favor, insira um CPF válido."})
        try :
            tipopost=request.user.usuario.tipo  
        except:
            tipopost=False      
        if request.POST.get("tipo") and tipopost==Tipo_usuario.objects.get(tipo="admin"):
            tipoform=request.POST.get("tipo")  
        else:
            tipoform="user" 
        if not (User.objects.filter(username=cpf)) :
            user=User.objects.create_user (username=cpf,first_name=first_name,last_name=last_name, email=email,password=senha)
            user.save()
            tipo=Tipo_usuario.objects.filter(tipo=tipoform).first()
            usuario=Usuario(usuario=user,cpf=cpf,tipo=tipo)
            usuario.save()
        else:
            messages.error(request, 'Usuário já existe')
        return render(request,"login.html")
    else:
        return render(request,"login.html")
def esqueceu_senha(request):
    if request.method=="GET":
        return render(request,"recuperar_senha.html")
    elif request.method=="POST":
        cpf=''.join(filter(str.isdigit, request.POST.get("cpf")))
        usuario = Usuario.objects.filter(cpf=cpf).first()
        nova_senha=gera_senha(15) 
        if not usuario:
            messages.error(request, 'Usuário já existe')
            return render(request,"recuperar_senha.html")
        body=f"""<html>
                <head></head>
                <body>
                    <h2>Olá {usuario.usuario.first_name}!</h2>
                    <p>Sua senha foi redefinida com sucesso.</p>
                    <p>Os dados para login são:</p>
                    <p>Seu nome de usuário: {usuario.cpf}</p>
                    <p>Sua senha provisória: {nova_senha}</p>
                    <p>O link para acesso ao sistema é: <a href="http://protuario-cloud.com.br"> protuario-cloud.com.br </p>
                    <p>Obrigado!</p>
                    <p> Administrador do Sistema</p>
                </body>
                </html>"""
        try:
            retorno=enviar_email_background(subject="Recuperação de Senha",body=body,recipients=[usuario.usuario.email,"protuariocloud@gmail.com"])
            messages.warning(request,str(retorno))
            usuario.usuario.set_password(nova_senha)
            usuario.usuario.save()
            usuario.save()
            return render(request,"login.html")
        except Exception as e:
            messages.error(request, 'Erro ao recuperar senha, favor entrar em contato com o administrador'+str(e))
    return render(request,"recuperar_senha.html")