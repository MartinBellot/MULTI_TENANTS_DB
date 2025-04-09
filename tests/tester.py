#!/usr/bin/env python
import requests
import getpass

# ----- Configuration -----
# URL du token endpoint sur le serveur Master
TOKEN_URL = "http://127.0.0.1:8000/o/token/"
# URL de la route protégée dans le projet Tenant
PROTECTED_URL = "http://127.0.0.1:8666/testapp/test/"

# Les identifiants du client OAuth (configurés dans l'admin de Master)
CLIENT_ID = "FJFLMVUmDMU09wEFMwXMvkJrsMzIcLWMFMHgKVWM"
CLIENT_SECRET = "9Pfg2zGGoV6d7u0rmE3c329cqEfXR6favCsmtefUCuINSse4LvnCj64PAhkgA0EOtYTUllmxxLEwpxeOBWC3C9rKYMGmGFjoFSNXBQCaQv0IWko6bEJcJjz159Zd4EDs"

def get_token(username, password):
    """
    Récupère un token d'accès depuis le serveur Master en utilisant le flow
    Resource Owner Password Credentials.
    """
    data = {
        "grant_type": "password",
        "username": username,
        "password": password,
    }
    print(f"Demande de token à {TOKEN_URL} avec l'utilisateur {username}...")
    # Envoi des credentials du client via HTTP Basic Auth
    response = requests.post(TOKEN_URL, data=data, auth=(CLIENT_ID, CLIENT_SECRET))
    response.raise_for_status()
    token_data = response.json()
    access_token = token_data.get("access_token")
    if not access_token:
        raise ValueError("Aucun token reçu. Vérifiez la configuration OAuth.")
    print("Token obtenu avec succès.")
    return access_token

def test_protected_resource(access_token):
    """
    Appelle la ressource protégée dans le projet Tenant en transmettant
    le token dans le header Authorization.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    print(f"\nAccès à la ressource protégée via {PROTECTED_URL} avec le header:")
    print(headers)
    response = requests.get(PROTECTED_URL, headers=headers)
    print("Code HTTP:", response.status_code)
    try:
        data = response.json()
    except Exception:
        data = response.text
    print("Réponse:", data)
    return response

def main():
    print("=== Test interactif de l'authentification OAuth2 ===")
    # Demande des identifiants à l'utilisateur
    username = input("Entrez votre adresse email (username) pour le serveur Master: ")
    password = getpass.getpass("Entrez votre mot de passe: ")
    
    # Récupération du token d'accès depuis le Master
    token = get_token(username, password)
    print("\n--- Token d'accès ---")
    print(token)
    
    # Appel de la ressource protégée dans le Tenant
    print("\n--- Test de la ressource protégée ---")
    test_protected_resource(token)

if __name__ == "__main__":
    main()