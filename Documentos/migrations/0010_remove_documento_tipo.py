# Generated by Django 4.2.17 on 2025-02-16 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Documentos", "0009_documento_tipo"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="documento",
            name="tipo",
        ),
    ]
