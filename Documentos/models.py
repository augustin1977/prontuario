from django.db import models
from Usuario_django.models import Usuario  # Supondo que seu modelo de usuário esteja em Usuario_django

class PermissaoDocumento(models.Model):
    usuario_concedente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='permissoes_concedidas')
    usuario_permitido = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='permissoes_recebidas')
    data_concessao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario_concedente', 'usuario_permitido')  # Evita duplicações

    def __str__(self):
        return f"{self.usuario_concedente.cpf} concedeu permissão a {self.usuario_permitido.cpf}"

class Tipo_documento(models.Model):
    tipo=models.TextField(max_length=255,default=None)
    def __str__(self):
        return self.tipo
    
class Documento(models.Model):
    proprietario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='documentos_proprietario')
    titulo= models.CharField(max_length=255,blank=False,null=False)
    resumo = models.TextField(blank=True,null=True)  # Conteúdo do documento
    arquivo = models.FileField(upload_to='protected/', blank=True, null=True)
    data_documento=models.DateTimeField()
    data_criacao = models.DateTimeField(auto_now_add=True)  # Data de criação do documento
    data_modificacao=models.DateTimeField(auto_now=True)
    secreto=models.BooleanField(blank=False,null=False,default=False)
    tipo=models.ForeignKey(Tipo_documento, on_delete=models.CASCADE, ) 

    def __str__(self):
        return f"Documento de {self.proprietario.cpf}"

    def pode_visualizar(self, usuario):
        """Verifica se um usuário pode visualizar o documento."""
        if self.proprietario == usuario:
            return True
        if self.secreto==True:
            return False
        # Verifica se o usuário tem permissão para ver todos os documentos do proprietário
        return PermissaoDocumento.objects.filter(
            usuario_concedente=self.proprietario,
            usuario_permitido=usuario
        ).exists()

    def pode_editar(self, usuario):
        """Verifica se um usuário pode editar o documento."""
        return self.proprietario == usuario  # Somente o proprietário pode editar

    def pode_excluir(self, usuario):
        """Verifica se um usuário pode excluir o documento."""
        return self.proprietario == usuario  # Somente o proprietário pode excluir

