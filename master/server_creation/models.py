from django.db import models
from django.utils import timezone

class TenantServer(models.Model):
    name = models.CharField(max_length=100, help_text="Nom court du serveur")
    ip_address = models.GenericIPAddressField(help_text="Adresse IP publique du serveur")
    port = models.PositiveIntegerField(help_text="Port d'exposition du serveur Tenant")
    client_id = models.CharField(max_length=100, help_text="Client ID OAuth attribué")
    secret = models.CharField(max_length=255, help_text="Secret OAuth (en clair, affiché temporairement avant chiffrement)")
    deployed_at = models.DateTimeField(default=timezone.now)
    
    # Paramètres pour le superuser (affichés en clair, à usage temporaire avant chiffrement ou sauvegarde sécurisée)
    django_superuser_username = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text="Nom d'utilisateur pour le superuser du Tenant"
    )
    django_superuser_email = models.EmailField(
        max_length=254,
        blank=True,
        null=True,
        help_text="Email pour le superuser du Tenant"
    )
    django_superuser_password = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Mot de passe pour le superuser du Tenant (affiché temporairement en clair)"
    )

    def __str__(self):
        return f"{self.name} ({self.ip_address}:{self.port})"