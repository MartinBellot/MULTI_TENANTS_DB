# files/utils.py
import hmac
import hashlib
import base64
from django.conf import settings

def generate_token(keyword: str) -> str:
    """
    Génère un token basé sur un HMAC pour un mot-clé.
    """
    secret_key = getattr(settings, 'SEARCH_ENC_KEY', 'default_secret_key').encode()
    # Normalisation du mot-clé
    msg = keyword.strip().lower().encode('utf-8')
    hm = hmac.new(secret_key, msg=msg, digestmod=hashlib.sha256)
    token_bytes = hm.digest()
    # Encodage en base64 pour simplifier le stockage
    return base64.urlsafe_b64encode(token_bytes).decode('utf-8')