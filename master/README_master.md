# Master Auth & App Management - Plateforme Django OAuth2

## 📝 Description

Ce projet Django agit comme **serveur central d’authentification OAuth2** avec :
- Une interface d’administration
- Un tableau de bord utilisateur
- Un système de gestion des applications OAuth2 créées par les développeurs (via `devapps`)

Il est conçu pour fonctionner avec des **tenants indépendants** qui se connectent à ce backend principal pour gérer l'authentification et la communication via des tokens sécurisés.

## 📁 Structure des dossiers (Master)

```
master/
├── accounts/           # Utilisateurs personnalisés (CustomUser)
├── devapps/            # Création d'applications OAuth2
├── frontend/           # Accueil & tableau de bord
├── server_creation/    # Déploiement auto de tenants (optionnel)
├── templates/          # Fichiers HTML
├── static/             # CSS, JS, images...
├── .env                # Variables d'environnement
├── Dockerfile
├── entrypoint.sh       # Script Docker de démarrage
└── manage.py
```

---

## 🚀 Démarrage avec Docker

```bash
git clone https://github.com/MartinBellot/MULTI_TENANTS_DB
cd master
docker-compose up -d --build
```

---

## 🔐 OAuth2 - Fonctionnalités

- **Token endpoint** : `/o/token/`
- **Introspection endpoint** : `/o/introspect/`
- **Enregistrement d’application** : `/devapps/register/`
- **Liste des applications créées** : `/devapps/list/`

---

## 🧪 Exemple d’intégration front :

```html
<a href="{% url 'oauth_login' %}" class="btn btn-warning">
  Se connecter avec MONRESEAU
</a>
```

---

## 🔒 Détails sur le chiffrement et la recherche

---

## 👤 Utilisateur par défaut

- **Email** : `gui.coquemont@gmail.com`
- **Mot de passe** : `adminpassword`

---
