# Generated by Django 4.2.17 on 2025-01-07 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Usuario_django", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tipo_usuario",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("tipo", models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name="usuario",
            name="tipo",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="Usuario_django.tipo_usuario",
            ),
            preserve_default=False,
        ),
    ]
