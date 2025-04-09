# tenant_project/core/authentication.py
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

class MasterIntrospectionAuthentication(BaseAuthentication):
    """
    Authentifie la requête en interrogeant l'endpoint d'introspection du serveur Master.
    Si l'utilisateur n'existe pas dans le Tenant, on le crée automatiquement.
    """
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None  # Aucun header n'est fourni
        
        try:
            scheme, token = auth_header.split()
        except ValueError:
            raise exceptions.AuthenticationFailed("Format d'authorization invalide.")
        
        if scheme.lower() != 'bearer':
            return None
        
        introspection_url = settings.OAUTH2_INTROSPECTION_URL  # ex: 'http://127.0.0.1:8000/o/introspect/'
        data = {'token': token}
        auth = (settings.OAUTH2_CLIENT_ID, settings.OAUTH2_CLIENT_SECRET)
        
        response = requests.post(introspection_url, data=data, auth=auth)
        if response.status_code != 200:
            raise exceptions.AuthenticationFailed("Échec de l’introspection du token.")
        
        result = response.json()
        if not result.get('active'):
            raise exceptions.AuthenticationFailed("Token inactif ou invalide.")
        print("Résultat de l'introspection:", result)  # Pour debug
        
        # Tenter de récupérer l'identifiant utilisateur
        user_identifier = result.get('user_email') or result.get('username')
        if not user_identifier:
            raise exceptions.AuthenticationFailed("Informations utilisateur introuvées dans le token.")
        
        User = get_user_model()
        try:
            user = User.objects.get(email=user_identifier)
        except User.DoesNotExist:
            # Auto-provisionnement : création automatique de l'utilisateur dans le Tenant
            user = User.objects.create_user(
                username=user_identifier,
                email=user_identifier,
                password=User.objects.make_random_password()
            )
            print(f"Création automatique de l'utilisateur {user_identifier} dans le Tenant.")
        except Exception as e:
            raise exceptions.AuthenticationFailed(f"Erreur lors de la récupération de l'utilisateur: {str(e)}")
        
        return (user, token)