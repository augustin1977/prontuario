from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from .models import *
from autenticacao import *
from auxiliares import validar_cpf


@is_user
def logout(request):
    django_logout(request)
    return redirect("login")

@is_user
def home(request):
    return render(request,"home.html")

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
    return redirect("login")

def cadastro(request):
    is_admin_user = request.user.is_authenticated and request.user.usuario.tipo.tipo == 'admin'
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

@is_super_user
def super_user(request):
    return render(request,"super_user.html")

@is_admin
def admin(request):
    return render(request,"administrador.html")