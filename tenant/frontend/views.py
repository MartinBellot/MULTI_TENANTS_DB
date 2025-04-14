from django.shortcuts import render, redirect
from django.conf import settings
import requests

def login_view(request):
    """
    Affiche le formulaire de connexion et récupère le token depuis le serveur Master.
    """
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Construire l'URL du token (définie dans settings.py du Tenant)
        token_url = settings.MASTER_TOKEN_URL  # par exemple : "http://127.0.0.1:8000/o/token/"
        client_id = settings.OAUTH2_CLIENT_ID
        client_secret = settings.OAUTH2_CLIENT_SECRET

        data = {
            "grant_type": "password",
            "username": username,
            "password": password,
        }
        # Demande de token au serveur Master via HTTP Basic Auth
        response = requests.post(token_url, data=data, auth=(client_id, client_secret))
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")
            # Sauvegarder le token dans la session pour la navigation ultérieure
            request.session['access_token'] = access_token
            request.session['user_email'] = username  # vous pouvez adapter si l'introspection renvoie d'autres infos
            return redirect('home')
        else:
            try:
                error = response.json().get("error", "Erreur inconnue")
            except Exception:
                error = "Erreur d'authentification"

    return render(request, "frontend/login.html", {"error": error})
