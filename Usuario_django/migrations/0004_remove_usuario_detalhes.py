# Generated by Django 4.2.17 on 2025-01-27 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Usuario_django", "0003_usuario_cpf"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="usuario",
            name="detalhes",
        ),
    ]
