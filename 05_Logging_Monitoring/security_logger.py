import logging
import json
from datetime import datetime

# Configuration d'un logger spécifique pour la sécurité
security_logger = logging.getLogger('SecurityAudit')
security_logger.setLevel(logging.INFO)

class SecurityAudit:
    @staticmethod
    def log_event(event_type, user_id, status, metadata=None):
        """
        Génère un log structuré (JSON) pour être facilement parsé par un SIEM (Splunk, ELK, Datadog)
        """
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type, # ex: AUTH_ATTEMPT, ACCESS_DENIED, DATA_EXPORT
            "user_id": user_id,
            "status": status, # SUCCESS / FAILURE
            "severity": "HIGH" if status == "FAILURE" else "INFO",
            "metadata": metadata or {}
        }
        
        # On logue en JSON pour faciliter l'indexation et l'alerte automatique
        security_logger.info(json.dumps(audit_entry))


# --- Cas pratique : Tentative d'IDOR détectée ---
def update_user_profile(requesting_user_id, target_user_id):
    if requesting_user_id != target_user_id:
        # 1. On bloque l'action (AuthZ du Jour 2)
        # 2. ON LOGUE LA TENTATIVE (Le réflexe Jour 6)
        SecurityAudit.log_event(
            event_type="UNAUTHORIZED_ACCESS_ATTEMPT",
            user_id=requesting_user_id,
            status="FAILURE",
            metadata={
                "target_resource": f"user_profile_{target_user_id}",
                "reason": "Ownership mismatch (Potential IDOR)"
            }
        )
        return {"error": "Forbidden"}, 403

    # Si OK
    SecurityAudit.log_event("PROFILE_UPDATE", requesting_user_id, "SUCCESS")
    return {"status": "Updated"}, 200