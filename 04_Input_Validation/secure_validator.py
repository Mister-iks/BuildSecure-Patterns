# Fichier : 04_Input_Validation/secure_validator.py
import re

class InputValidator:
    @staticmethod
    def validate_user_registration(data):
        # 1. Vérification de la présence des champs (Structure)
        required_fields = ['username', 'email', 'age']
        if not all(field in data for field in required_fields):
            raise ValueError("Structure de requête invalide.")

        # 2. Validation de Type & Contraintes (Type & Range)
        if not isinstance(data['age'], int) or not (18 <= data['age'] <= 120):
            # On bloque les injections via le type et les valeurs métier aberrantes
            raise ValueError("Âge invalide : doit être un entier entre 18 et 120.")

        # 3. Validation par Liste Blanche (Allow-listing)
        # On ne permet que les caractères alphanumériques pour le pseudo
        if not re.match(r"^[a-zA-Z0-9_]{3,20}$", data['username']):
            raise ValueError("Le pseudo contient des caractères interdits.")

        # 4. Validation de Format (Domain Specific)
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", data['email']):
            raise ValueError("Format d'email invalide.")

        return True

# --- Application ---
raw_input = {"username": "admin'--", "email": "hacker@evil.com", "age": 25}

try:
    if InputValidator.validate_user_registration(raw_input):
        # Seulement ici, on traite la donnée (ex: écriture en DB)
        print("Données validées et sécurisées.")
except ValueError as e:
    # On logue l'erreur pour le monitoring (Jour 6 ?)
    print(f"Tentative invalide : {e}")