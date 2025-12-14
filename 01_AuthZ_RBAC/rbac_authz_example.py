# Pseudo-code Python - La fonction de vérification d'Autorisation (AuthZ)

def check_permission(user_token_id: int, user_role: str, target_user_id: int) -> bool:
    
    # 1. Verification d'accès par ROLE (la politique de l'entreprise)
    if user_role in ['ADMIN', 'MANAGER']:
        # Les rôles supérieurs peuvent agir sur tout le monde (accès total)
        return True
    
    # 2. Verification d'accès par PROPRIÉTÉ (la sécurité fondamentale)
    # Si le rôle est "CLIENT" ou "USER", il ne doit modifier QUE son propre compte
    if user_token_id == target_user_id:
        return True
    
    # 3. Échec de la vérification
    # Le user est un "CLIENT" et tente d'accéder à un autre ID
    return False

# --- Utilisation sur votre endpoint ---

# Récupération de l'identité (AuthN) et des infos du jeton
current_user_id = token.get_user_id()
current_user_role = token.get_role()
target_user_id = request.url_params.get('target_user_id')

if not check_permission(current_user_id, current_user_role, target_user_id):
    # C'est ici que l'IDOR est stoppé net
    raise HTTPError(403, "Accès Interdit : Vous n'avez pas la permission sur cette ressource.")

# Si on arrive ici, l'action est autorisée (AuthZ OK)
process_request()