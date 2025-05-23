# Generated by Django 4.2.20 on 2025-04-15 07:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TenantServer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Nom court du serveur', max_length=100)),
                ('ip_address', models.GenericIPAddressField(help_text='Adresse IP publique du serveur')),
                ('port', models.PositiveIntegerField(help_text="Port d'exposition du serveur Tenant")),
                ('client_id', models.CharField(help_text='Client ID OAuth attribué', max_length=100)),
                ('secret', models.CharField(help_text='Secret OAuth (en clair, affiché temporairement avant chiffrement)', max_length=255)),
                ('deployed_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
