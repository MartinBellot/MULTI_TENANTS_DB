from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
import requests
from django.views.decorators.http import require_POST
from files.models import File
import os

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
        print(f"Response from token endpoint: {response.status_code} - {response.text}")
        if response.status_code == 200:
            
            token_data = response.json()
            access_token = token_data.get("access_token")
            # Sauvegarder le token dans la session pour la navigation ultérieure
            request.session['access_token'] = access_token
            request.session['user_email'] = username  # vous pouvez adapter si l'introspection renvoie d'autres infos

            created_by = os.environ.get("CREATED_BY", None)
            print("[DEBUG] CREATED_BY:", created_by)  # Pour debug
            print("[DEBUG] Utilisateur authentifié:", username)  # Pour debug

            if created_by != username:
                error = "Vous n'êtes pas le créateur de ce serveur."
                return render(request, "frontend/login.html", {"error": error})
            return redirect('home')
        else:
            try:
                error = response.json().get("error", "Erreur inconnue")
            except Exception:
                error = "Erreur d'authentification"

    return render(request, "frontend/login.html", {"error": error})

def home_view(request):
    """
    Page d'accueil accessible uniquement aux utilisateurs authentifiés.
    """
    access_token = request.session.get('access_token')
    print(f"Passer dans tenant frontend avec accesstoken : {access_token}")
    if not access_token:
        return redirect('login')
    files = File.objects.all()
    # Vous pouvez également faire appel à une API interne en utilisant le token.
    return render(request, "frontend/home.html", {"files": files})

@require_POST
def upload_file(request):
    # Récupérer le fichier uploadé
    uploaded_file = request.FILES.get('file_upload')
    # Récupérer le dossier sélectionné
    folder_id = request.POST.get('folder')
    
    if uploaded_file:
        # Créer et sauvegarder une instance de File
        file_instance = File.objects.create(
            original_name = uploaded_file.name,
            file_path = uploaded_file,
            # Vous pouvez sauvegarder ou utiliser folder_id si vous avez créé un champ correspondant dans le modèle
        )
        file_instance.save()
        
        return redirect('home')
    else:
        # Gérer le cas où aucun fichier n'a été uploadé
        return render(request, 'frontend/home.html', {'error': 'Aucun fichier sélectionné'})
    
def file_view(request, pk):
    file_obj = get_object_or_404(File, pk=pk)
    # Ouvrir le fichier en mode binaire
    try:
        with file_obj.file_path.open('rb') as f:
            encrypted_content = f.read()
        # Essayer de décoder en UTF-8 (utile pour un fichier texte)
        try:
            encrypted_text = encrypted_content.decode('utf-8')
        except UnicodeDecodeError:
            encrypted_text = "Le contenu du fichier n'est pas affichable en tant que texte."
    except Exception as e:
        encrypted_text = f"Erreur lors de la lecture du fichier : {e}"
    
    return render(request, 'frontend/files/file_view.html', {
        'file': file_obj,
        'encrypted_content': encrypted_text,
    })