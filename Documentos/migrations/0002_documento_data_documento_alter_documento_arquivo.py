# Generated by Django 4.2.17 on 2025-01-27 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Documentos", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="documento",
            name="data_documento",
            field=models.DateTimeField(default="2025-01-27 10:20:00.0"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="documento",
            name="arquivo",
            field=models.FileField(blank=True, null=True, upload_to=""),
        ),
    ]
