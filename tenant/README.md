# Tenant - Plateforme connectée au serveur OAuth2

## 📝 Description

Cette application Django représente un **tenant autonome** connecté à un serveur principal d’authentification OAuth2 (`master`). Elle permet l’upload sécurisé de fichiers, leur recherche via des mots-clés chiffrés, et une authentification centralisée via tokens.

> Chaque tenant est déployé dans un conteneur indépendant, avec sa propre base de données.


## 📁 Structure du projet

```
tenant/
│
├── files/               # Gestion des fichiers, upload, recherche sécurisée
├── frontend/            # Interface utilisateur (login, home)
├── core/authentication.py  # Authentification via introspection OAuth
├── templates/           # Templates HTML
├── media/               # Fichiers uploadés
├── staticfiles/         # CSS / JS / autres fichiers statiques
├── settings.py          # Paramètres Django spécifiques au tenant
├── urls.py              # Routes Django
├── entrypoint.sh        # Script de lancement avec génération automatique de SECRET_KEY
└── .env                 # Configuration (clé secrète, accès DB, credentials OAuth)
```
## 📘 Documentation des composants

- 🌍 [tenant](.) – Application autonome connectée au serveur OAuth2 principal
  - 📁 [files](files) – Gestion des fichiers du tenant
  - 💻 [frontend](frontend) – Interface utilisateur du tenant

## 🔐 Authentification centralisée OAuth2

Le tenant **ne gère aucun utilisateur localement**. Il délègue l’authentification au serveur principal (master) via :

- `http://master-web:8000/o/token/` (grant_type = password)
- `http://master-web:8000/o/introspect/` (vérification de token)
- L'utilisateur est automatiquement créé dans le tenant s'il n'existe pas (auto-provisioning).

```python
# core/authentication.py
user = User.objects.create_user(
    username=user_identifier,
    email=user_identifier,
    password=User.objects.make_random_password()
)
```


## 🔒 Détail du chiffrement & recherche sécurisée

### 1. Génération de mots-clés chiffrés

Chaque mot-clé est transformé en **token sécurisé (HMAC SHA-256)** stocké dans la table `FileKeyword`, sans jamais sauvegarder le mot-clé en clair.

```python
def generate_token(keyword: str) -> str:
    secret_key = settings.SEARCH_ENC_KEY.encode()
    msg = keyword.strip().lower().encode('utf-8')
    return base64.urlsafe_b64encode(hmac.new(secret_key, msg, hashlib.sha256).digest()).decode()
```

### 2. Recherche sécurisée

La recherche se fait uniquement via comparaison de **tokens HMAC** dans la base de données, évitant toute fuite d'information sensible.

```python
token = generate_token(user_input)
matching_files = FileKeyword.objects.filter(token=token)
```

> ✅ Ce mécanisme garantit que même l'administrateur ne peut lire les mots-clés initiaux.


## ⚙️ Lancer un tenant

```bash
cd tenant

# Lancer le conteneur
docker-compose up -d --build
```

Accès à l’interface : [http://localhost:8001](http://localhost:8001)


## ✉️ Configuration `.env`

```env
DEBUG=0
DJANGO_SECRET_KEY=  # Généré automatiquement si vide
DATABASE_URL=postgres://user:pass@db:5435/tenant_db

DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=gui.coquemont@gmail.com
DJANGO_SUPERUSER_PASSWORD=adminpassword

DB_HOST=db
DB_PORT=5435

# Liens vers le master (OAuth2)
MASTER_TOKEN_URL=http://master-web:8000/o/token/
OAUTH2_INTROSPECTION_URL=http://master-web:8000/o/introspect/
OAUTH2_CLIENT_ID=...
OAUTH2_CLIENT_SECRET=...
```


## 👤 Auteur

Projet réalisé dans le cadre d'un système multitenant sécurisé connecté à un backend d'authentification centralisée OAuth2.


## 🌐 Navigation

- [🏠 Projet Principal](../)
- [📁 master](../master/)
- [🔒 accounts](../master/accounts/)
- [🛠️ devapps](../master/devapps/)
- [💻 frontend](../master/frontend/)
- [🚀 server_creation](../master/server_creation/)
- [🌍 tenant](../tenant/)
- [📁 tenant/files](../tenant/files/)
- [💻 tenant/frontend](../tenant/frontend/)
