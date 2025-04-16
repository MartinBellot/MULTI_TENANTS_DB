# Readme.md master

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

## 📘 Documentation des composants https://github.com/MartinBellot/MULTI_TENANTS_DB/blob/readmes/master

- 🔒 [account](accounts) - Utilisateurs personnalisés

- 🔒 [devapps](devapps) - Création d'application OAuth2

- 🔒 [frontend](frontend) - Frontend de l'application 

- 🔒 [server_creation](server_creation) - Création de serveur OAuth2 
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


---

## 🌐 Navigation

## 🌐 Navigation

- [🏠 Projet Principal](../#readme)
- [📁 master](../master#readme)
- [🔒 accounts](../master/accounts#readme)
- [🛠️ devapps](../master/devapps#readme)
- [💻 frontend](../master/frontend#readme)
- [🚀 server_creation](../master/server_creation#readme)
- [🌍 tenant](../tenant#readme)
- [📁 tenant/files](../tenant/files#readme)
- [💻 tenant/frontend](../tenant/frontend#readme)
