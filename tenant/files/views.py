from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, HttpResponseRedirect, HttpResponse
from django.core.files.base import ContentFile
from django.conf import settings
from django.urls import reverse
from django.db.models import Q
import os
from cryptography.fernet import Fernet

from .forms import FileUploadForm, FileSearchForm
from .models import File, FileKeyword
from .utils import generate_token

import logging

logger = logging.getLogger(__name__)
print("Module files.views chargé", flush=True)

def file_list(request):
    """Liste des fichiers disponibles."""
    files = File.objects.order_by('-upload_date')
    return render(request, 'frontend/home.html', {'files': files})

def file_upload(request):
    print("Début de la fonction file_upload", flush=True)
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file_upload']
            file_data = uploaded_file.read()
            print(f"Fichier reçu : {uploaded_file.name}, taille : {len(file_data)} octets", flush=True)
            
            # Récupérer la clé de chiffrement depuis settings
            ENCRYPTION_KEY = getattr(settings, 'ENCRYPTION_KEY', None)
            if ENCRYPTION_KEY is None:
                ENCRYPTION_KEY = Fernet.generate_key()
                print("ENCRYPTION_KEY non défini dans settings, utilisation d'une clé générée automatiquement (mode test)", flush=True)
            cipher_suite = Fernet(ENCRYPTION_KEY)
            
            # Chiffrer le contenu du fichier avec Fernet
            encrypted_data = cipher_suite.encrypt(file_data)
            print(f"Chiffrement effectué pour le fichier : {uploaded_file.name}", flush=True)
            
            # Créer un ContentFile avec les données chiffrées et enregistrer l'instance
            encrypted_file = ContentFile(encrypted_data, name=uploaded_file.name)
            instance = form.save(commit=False)
            instance.file_path.save(uploaded_file.name, encrypted_file)
            instance.original_name = uploaded_file.name
            
            # Stocker une valeur indiquant que le fichier a été chiffré
            instance.iv = "Fernet"  
            instance.save()
            
            print(f"Fichier chiffré enregistré avec succès : {uploaded_file.name}", flush=True)
            return redirect('file_list')
        else:
            print("Form non valide", flush=True)
            print(form.errors, flush=True)
    else:
        print("Méthode GET détectée", flush=True)
        form = FileUploadForm()
    print("Affichage du formulaire", flush=True)
    return render(request, 'frontend/home.html', {'form': form,'files': File.objects.all()})

def file_download(request, pk):
    """Télécharger le fichier en le déchiffrant."""
    file_obj = get_object_or_404(File, pk=pk)
    
    # Ouvrir le fichier chiffré
    file_obj.file_path.open('rb')
    encrypted_data = file_obj.file_path.read()
    file_obj.file_path.close()
    print(f"Fichier chiffré lu depuis le disque : {file_obj.original_name}", flush=True)
    
    # Récupérer la clé de chiffrement depuis settings
    ENCRYPTION_KEY = getattr(settings, 'ENCRYPTION_KEY', None)
    if ENCRYPTION_KEY is None:
        ENCRYPTION_KEY = Fernet.generate_key()
        print("ENCRYPTION_KEY non défini dans settings lors du téléchargement, utilisation d'une clé générée automatiquement (mode test)", flush=True)
    cipher_suite = Fernet(ENCRYPTION_KEY)
    
    # Déchiffrer les données
    try:
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        print(f"Déchiffrement réussi pour le fichier : {file_obj.original_name}", flush=True)
    except Exception as e:
        print(f"Erreur lors du déchiffrement du fichier {file_obj.original_name} : {str(e)}", flush=True)
        return HttpResponse('Erreur lors du déchiffrement du fichier.', status=500)
    
    # Retourner une réponse HTTP avec le fichier déchiffré
    response = HttpResponse(decrypted_data, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{file_obj.original_name}"'
    return response

def file_search(request):
    """Rechercher un fichier par mot-clé."""
    if request.method == 'POST':
        form = FileSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            # Implémenter la logique de recherche selon vos besoins
            files = File.objects.filter(original_name__icontains=query)
            return render(request, 'files/file_list.html', {'files': files, 'search': True, 'query': query})
    else:
        form = FileSearchForm()
    return render(request, 'files/file_search.html', {'form': form})

from django.views.decorators.http import require_POST

@require_POST
def file_delete(request, pk):
    """Supprimer un fichier (et son contenu chiffré)."""
    file_obj = get_object_or_404(File, pk=pk)
    print(f"Suppression du fichier : {file_obj.original_name}", flush=True)
    file_obj.file_path.delete(save=False)  # Supprime le fichier du disque
    file_obj.delete()  # Supprime l'entrée en base
    return redirect('file_list')