# Generated by Django 5.1.4 on 2024-12-24 01:07

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_client_collaborators'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='cnpj',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='collaborators',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
