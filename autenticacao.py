from django.contrib.auth.models import User
from Usuario_django.models import *
from django.contrib.auth import authenticate
from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib import messages


def is_user(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            usuario= request.user
        except:
            usuario=False
        if usuario:
            if usuario.is_authenticated and Usuario.objects.filter(usuario=usuario).first():
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, 'Acesso negado')
                return redirect('login')
        else:
            messages.error(request, 'Acesso negado')
            return redirect('login')  # Redireciona para uma página de login ou qualquer outra página apropriada
    return wrapper
def is_super_user(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            user= request.user
        except:
            user=False
        if user:
            if user.is_authenticated and Usuario.objects.filter(usuario=user).first():
                usuario= Usuario.objects.filter(usuario=user).first()
                filter= Q(tipo="super_user")|Q(tipo="admin")
                tipo= Tipo_usuario.objects.filter(filter)
                if usuario.tipo in tipo:
                    return view_func(request, *args, **kwargs)
                else:
                    messages.error(request, 'Acesso negado')
                    return redirect('login')
            else:
                messages.error(request, 'Acesso negado')
                return redirect('login')
        else:
            messages.error(request, 'Acesso negado')
            return redirect('login')  # Redireciona para uma página de login ou qualquer outra página apropriada
    return wrapper

def is_admin(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            user= request.user
        except:
            user=False
        if user:
            if user.is_authenticated:
                usuario= Usuario.objects.filter(usuario=user).first()
                tipo= Tipo_usuario.objects.get(tipo="admin")
                if usuario.tipo==tipo:
                    return view_func(request, *args, **kwargs)
                else:
                    messages.error(request, 'Acesso negado')
                    return redirect('home')
            else:
                messages.error(request, 'Acesso negado')
                return redirect('login')
        else:
            messages.error(request, 'Acesso negado')
            return redirect('login')  # Redireciona para uma página de login ou qualquer outra página apropriada
    return wrapper