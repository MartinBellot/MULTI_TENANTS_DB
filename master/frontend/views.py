from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

def home(request):
    form = CustomAuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/dashboard/')
    return render(request, 'home.html', {'form': form})

@login_required
def dashboard(request):
    user_files = CustomUser.objects.filter(id=request.user.id)
    return render(request, 'dashboard.html', {'user_files': user_files})
    
@require_http_methods(["GET"])
def launch_new_server(request):
    # Ici, vous pouvez ajouter la logique qui lance réellement le serveur
    # (exemple : appeler un script, démarrer un processus, etc.)
    return HttpResponse("Le nouveau serveur a été lancé avec succès !")

@require_http_methods(["GET", "POST"])
def create_tenant(request):
    if request.method == "POST":
        # Traitement de la création d'un tenant à partir des données envoyées par le formulaire
        # Par exemple : validation et sauvegarde d’un tenant dans la BDD
        return HttpResponse("Tenant créé avec succès !")
    return render(request, "create_tenant.html")