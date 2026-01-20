import jwt
import datetime

SECRET_KEY = "VOTRE_CLE_TRES_LONGUE_ET_COMPLEXE_GENEREE_VIA_VAULT"

def create_secure_token(user_id, roles):
    payload = {
        "sub": user_id,
        "roles": roles,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15) # Expiration courte !
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token):
    try:
        # On force l'algorithme pour éviter l'attaque "alg: none"
        decoded_payload = jwt.decode(
            token, 
            SECRET_KEY, 
            algorithms=["HS256"]
        )
        return decoded_payload
    except jwt.ExpiredSignatureError:
        print("Alerte : Token expiré.")
    except jwt.InvalidTokenError:
        # Ici on logue l'événement pour notre Security Logger du Jour 6 !
        print("Alerte Sécurité : Tentative d'utilisation d'un token corrompu.")
    return None

# --- Pratique : Ne jamais mettre de secrets dans le payload ---
# MAUVAIS : "payload": {"user": "admin", "db_password": "123"}
# BON : "payload": {"sub": "12345", "scope": "read:profile"}