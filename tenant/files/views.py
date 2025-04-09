# files/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
from django.db.models import Q
import os

from .forms import FileUploadForm, FileSearchForm
from .models import File, FileKeyword
from .utils import generate_token

def file_list(request):
    """Liste des fichiers disponibles."""
    files = File.objects.order_by('-upload_date')
    return render(request, 'files/file_list.html', {'files': files})

def file_upload(request):
    """Uploader un nouveau fichier."""
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('file_list')
    else:
        form = FileUploadForm()
    return render(request, 'files/file_upload.html', {'form': form})

def file_search(request):
    """Rechercher un fichier par mot-clé."""
    if request.method == 'POST':
        form = FileSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            token = generate_token(query)
            # On récupère les file_ids dont le token correspond
            matching_keywords = FileKeyword.objects.filter(token=token).select_related('file')
            files = [kw.file for kw in matching_keywords]
            return render(request, 'files/file_list.html', {'files': files, 'search': True, 'query': query})
    else:
        form = FileSearchForm()
    return render(request, 'files/file_search.html', {'form': form})

def file_download(request, pk):
    """Télécharger le fichier original."""
    file_obj = get_object_or_404(File, pk=pk)
    file_path = file_obj.file_path.path
    # On renvoie une réponse de type FileResponse
    file_handle = open(file_path, 'rb')
    response = FileResponse(file_handle, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
    return response