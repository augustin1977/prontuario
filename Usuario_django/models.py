from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tipo_usuario(models.Model):
    tipo=models.CharField(max_length=50)
    def __str__(self):
        return self.tipo
class Usuario(models.Model):
    usuario=models.OneToOneField(User, verbose_name=("Usuario"), on_delete=models.CASCADE,primary_key=True,)
    cpf=models.CharField(max_length=30,unique=True)
    tipo=models.ForeignKey(Tipo_usuario, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.usuario.username} - {self.tipo}"