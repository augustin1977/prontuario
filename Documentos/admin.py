from django.contrib import admin
from .models import *

admin.site.register(Documento)
admin.site.register(PermissaoDocumento)
admin.site.register(Tipo_documento)