# Master Auth & App Management - Plateforme Django OAuth2

## 📝 Description

Ce projet Django agit comme **serveur central d’authentification OAuth2** avec une interface d’administration, un tableau de bord utilisateur et un système de gestion des applications OAuth créées par des développeurs (devapps).

Il est conçu pour fonctionner avec un système de tenants indépendants qui se connectent à ce backend principal.


## 🔧 Technologies utilisées

- Python 3.10.12
- Django 4.2.20
- Django REST Framework (DRF) 3.16.0
- Django OAuth Toolkit
- PostgreSQL
- Docker & Docker Compose
- Gunicorn

---


## 📁 Structure
master/ │ ├── accounts/ # Gestion des utilisateurs personnalisés (CustomUser) ├── frontend/ # Pages d'accueil et tableau de bord ├── devapps/ # Création & gestion d'applications OAuth2 ├── server_creation/ # (optionnel) pour déploiement de tenants ├── templates/ # Templates partagés ├── static/ # Fichiers statiques (styles.css) ├── .env # Variables d'environnement └── entrypoint.sh #


## 📘 Documentation des composants

- 🔒 [master](https://github.com/MartinBellot/MULTI_TENANTS_DB/blob/readmes/master) - Application 
  - 🔒 [master/accounts](https://github.com/MartinBellot/MULTI_TENANTS_DB/blob/readmes/master/accounts) – Gestion des utilisateurs personnalisés (CustomUser)
  - 🛠️ [master/devapps](https://github.com/MartinBellot/MULTI_TENANTS_DB/blob/readmes/master/devapps) – Création & gestion des applications OAuth2
  - 💻 [master/frontend](https://github.com/MartinBellot/MULTI_TENANTS_DB/blob/readmes/master/frontend) – Pages d'accueil et tableau de bord utilisateur
  - 🚀 [master/server_creation](https://github.com/MartinBellot/MULTI_TENANTS_DB/blob/readmes/master/server_creation) – Déploiement automatique de tenants
- 🌍 [tenant](https://github.com/MartinBellot/MULTI_TENANTS_DB/blob/readmes/tenant) – Application autonome connectée au serveur OAuth2 principal
  - 💻 [tenant/frontend](https://github.com/MartinBellot/MULTI_TENANTS_DB/blob/readmes/tenant/frontend) – Interface utilisateur du tenant
  - 📁 [tenant/files](https://github.com/MartinBellot/MULTI_TENANTS_DB/blob/readmes/tenant/files) – Gestion des fichiers du tenant

---

## Démarrage automatique via Docker
```bash
# Clone du repo
git clone https://github.com/MartinBellot/MULTI_TENANTS_DB
cd master

# Lancement des conteneurs
docker-commpose up -d --build
```

## 🔐 OAuth2 - Points clés

- Endpoint token : `/o/token/`
- Endpoint introspection : `/o/introspection/`
- Interface d'enregistrement : `/devapps/register/`
- Liste des apps crées : `/devapps/list/`


## 🧪 Exemple d'intégration front :
```html
<a href="{% url 'oauth_login' %}" class="btn btn-warning">
  Se connecter avec MONRESEAU
</a>
``` 

## 🧑 Connexion par défaut

- Email : `gui.coquemont@gmail.com`
- Mot de passe : `adminpassword`
