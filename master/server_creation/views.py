# server_creation/views.py
import docker
import secrets
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from .forms import ServerCreationForm
from .models import TenantServer
import os
from oauth2_provider.models import Application
from django.contrib.auth.decorators import login_required

@login_required
def server_list(request):
    """Affiche la liste des serveurs déployés avec leur statut de container."""
    servers = TenantServer.objects.all().order_by('-deployed_at')
    status_dict = {}
    try:
        client = docker.from_env()
    except Exception as e:
        # Si Docker n'est pas accessible, on marque tous les statuts à "inconnu"
        for server in servers:
            status_dict[server.id] = "inconnu"
    else:
        for server in servers:
            container_name = f"tenant_{server.name}"
            try:
                container = client.containers.get(container_name)
                status_dict[server.id] = container.status  # Ex: "running", "exited", etc.
            except docker.errors.NotFound:
                status_dict[server.id] = "non trouvé"
            except Exception as e:
                status_dict[server.id] = "erreur"
    
    return render(request, 'server_creation/server_list.html', {'servers': servers, 'status_dict': status_dict})

@login_required
def server_create(request):
    """
    Déploie un nouveau serveur Tenant.
    """
    if request.method == 'POST':
        form = ServerCreationForm(request.POST)
        print('Form data:', request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            port = form.cleaned_data['port']
            su_username = form.cleaned_data['superuser_username']
            su_email = form.cleaned_data['superuser_email']
            su_password = form.cleaned_data['superuser_password']

            print(f"Nom du serveur: {name}, Port: {port}")
            
            plain_secret = secrets.token_urlsafe(32)
            client_id = secrets.token_hex(8)

            try:
                oauth_app = Application.objects.create(
                    user=request.user,  # ou un utilisateur par défaut si besoin
                    name=f"{name} Tenant App",
                    client_type=Application.CLIENT_CONFIDENTIAL,
                    authorization_grant_type=Application.GRANT_PASSWORD,
                    hash_client_secret=False,
                    redirect_uris="",  # Pour le grant type "password", ce champ n'est pas utilisé
                )
                generated_client_id = oauth_app.client_id
                generated_client_secret = oauth_app.client_secret
                generated_hash_client_secret = oauth_app.hash_client_secret
                print("Hash du secret: ", generated_hash_client_secret)
                print("Application OAuth créée: ", generated_client_id, generated_client_secret)
            except Exception as e:
                print(f"Erreur lors de la création de l'application OAuth: {e}")
                messages.error(request, f"Erreur lors de la création de l'application OAuth: {str(e)}")
                return render(request, 'server_creation/server_create.html', {'form': form})

            try:
                print("Tentative de connexion au client Docker...")
                client = docker.from_env()
                print("Client Docker connecté.", client.ping)
                
                # Obtenir le chemin absolu vers le répertoire tenants.
                TENANTS_DIR = getattr(settings, 'TENANTS_SOURCE_DIR', '/app/tenant')
                print(f"Chemin de build utilisé: {TENANTS_DIR}")

                # Vérifier si le répertoire existe
                if not os.path.exists(TENANTS_DIR):
                    raise FileNotFoundError(f"Le répertoire {TENANTS_DIR} n'existe pas.")
                print("Liste des fichiers dans le répertoire:", os.listdir(TENANTS_DIR))

                database_url = f"postgres://youruser:yourpassword@tenant_{name}_db:5435/tenant_{name}_db"
                print("DATABASE_URL pour le tenant :", database_url)
                
                # Tenter de construire l'image tenant-server
                try:
                    image, build_logs = client.images.build(
                        path=TENANTS_DIR,
                        tag="tenant-server:latest"
                    )
                    print("Image construite avec succès.")
                except Exception as build_error:
                    print(f"Erreur lors de la construction de l'image: {build_error}")
                    # Si l'image existe déjà, on continue
                    # Note : tu pourrais vérifier précisément l'erreur et décider de ne pas échouer
                                    
                # Tenter de lancer le container
                container = client.containers.run(
                    image="tenant-server:latest",
                    name=f"tenant_{name}",
                    environment={
                        "TENANT_NAME": name,
                        "CLIENT_ID": client_id,
                        "CLIENT_SECRET": plain_secret,
                        "DB_HOST": f"tenant_{name}_db",
                        "DB_PORT": "5435",  # Port interne du container Postgres
                        "DATABASE_URL": database_url,
                        "DJANGO_SUPERUSER_USERNAME": su_username,
                        "DJANGO_SUPERUSER_EMAIL": su_email,
                        "DJANGO_SUPERUSER_PASSWORD": su_password,
                        "CLIENT_ID": generated_client_id,
                        "CLIENT_SECRET": generated_client_secret,
                        "CREATED_BY": request.user.email,
                    },
                    ports={'8001/tcp': port},
                    detach=True,
                    network=settings.DEPLOYMENT_NETWORK
                )
                db_container = client.containers.run(
                    image="postgres:13",
                    name=f"tenant_{name}_db",
                    environment={
                        "POSTGRES_DB": f"tenant_{name}_db",
                        "POSTGRES_USER": "youruser",
                        "POSTGRES_PASSWORD": "yourpassword",
                        "PGPORT": "5435",  # Le port interne du container Postgres
                    },
                    # On mappe le port 5435 interne au même port sur l'hôte (ou adapte si tu veux un port dynamique)
                    ports={'5435/tcp': 5435},
                    detach=True,
                    # Création d'un volume nommé spécifique pour le DB
                    volumes={f"db_{name}": {'bind': '/var/lib/postgresql/data', 'mode': 'rw'}},
                    network=settings.DEPLOYMENT_NETWORK
                )
                print("Container lancé avec succès.")
            except Exception as e:
                print(f"Erreur lors du déploiement du serveur: {e}")
                messages.error(request, f"Erreur lors du déploiement: {str(e)}")
                return render(request, 'server_creation/server_create.html', {'form': form})
            
            ip_address = "127.0.0.1"

            new_server = TenantServer.objects.create(
                name=name,
                ip_address=ip_address,
                port=port,
                client_id=client_id,
                secret=plain_secret,
                django_superuser_username=su_username,
                django_superuser_email=su_email,
                django_superuser_password=su_password,
                created_by=request.user,
            )
            messages.success(request, f"Serveur '{name}' déployé avec succès ! Secret: {plain_secret}")
            return redirect('server_creation:server_list')
    else:
        form = ServerCreationForm()
    
    return render(request, 'server_creation/server_create.html', {'form': form})


@login_required
def server_stop(request, pk):
    """
    Arrête le container du serveur Tenant identifié par pk.
    """
    server = get_object_or_404(TenantServer, pk=pk)
    try:
        client = docker.from_env()
        # On suppose que le container a été nommé "tenant_<name>"
        container_name = f"tenant_{server.name}"
        container = client.containers.get(container_name)
        container.stop()
        # Arreter la DB:
        db_container_name = f"tenant_{server.name}_db"
        db_container = client.containers.get(db_container_name)
        db_container.stop()
        messages.success(request, f"Serveur '{server.name}' arrêté avec succès.")
    except Exception as e:
        messages.error(request, f"Erreur lors de l'arrêt du serveur '{server.name}': {e}")
    return redirect('server_creation:server_list')


@login_required
def server_start(request, pk):
    """
    Démarre le container du serveur Tenant identifié par pk.
    """
    server = get_object_or_404(TenantServer, pk=pk)
    try:
        client = docker.from_env()
        container_name = f"tenant_{server.name}"
        container = client.containers.get(container_name)
        container.start()
        messages.success(request, f"Serveur '{server.name}' démarré avec succès.")
    except Exception as e:
        messages.error(request, f"Erreur lors du démarrage du serveur '{server.name}': {e}")
    return redirect('server_creation:server_list')

@login_required
def server_restart(request, pk):
    """
    Redémarre le container du serveur Tenant identifié par pk.
    """
    server = get_object_or_404(TenantServer, pk=pk)
    try:
        client = docker.from_env()
        container_name = f"tenant_{server.name}"
        container = client.containers.get(container_name)
        container.restart()
        messages.success(request, f"Serveur '{server.name}' redémarré avec succès.")
    except Exception as e:
        messages.error(request, f"Erreur lors du redémarrage du serveur '{server.name}': {e}")
    return redirect('server_creation:server_list')