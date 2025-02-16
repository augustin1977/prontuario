import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Usuario.settings")
django.setup()
from Usuario.settings import *
from Usuario_django.models import *
from Documentos.models import *

# Configurar o Django para rodar o script independentemente
  # Substitua 'seu_projeto' pelo nome do seu projeto



def cria_registros():
    
# Lista de especialidades médicas
    especialidades_medicas = [
        "Cardiologia", "Endocrinologia", "Gastroenterologia", "Hematologia",
        "Infectologia", "Nefrologia", "Neurologia", "Oftalmologia", "Oncologia",
        "Ortopedia", "Otorrinolaringologia", "Pediatria", "Pneumologia","Cirurgia",
        "Psiquiatria", "Reumatologia", "Urologia", "Dermatologia","Odontologia",
        "Ginecologia", "Obstetrícia", "Clínica Geral", "Medicina do Trabalho",
        "Radiologia", "Patologia", "Anestesiologia","Geriatria","Reumatologia","Sem especialidade"
    ]
    tipos_usuarios=["user","admin","super_user","medico"]
    especialidades_medicas.sort()
    for tipo in especialidades_medicas:
        obj, criado = Tipo_documento.objects.get_or_create(tipo=tipo)
    for usuario in tipos_usuarios:
        obj, criado = Tipo_usuario.objects.get_or_create(tipo=usuario)
    tipos=Tipo_documento.objects.all()
    for documento in Documento.objects.all():
        if documento.tipo not in tipos:
            documento.tipos=Tipo_documento.objects.filter(tipo="Sem especialidade").save()
            

if __name__ == "__main__":
    cria_registros()