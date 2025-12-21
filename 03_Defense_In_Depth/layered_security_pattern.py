class SecureTransactionHandler:
    def __init__(self, user_context, request_data):
        self.user = user_context
        self.data = request_data

    def execute_virement(self):
        try:
            # COUCHE 1 : Validation de l'intégrité (Input Validation)
            self._validate_input()
            
            # COUCHE 2 : Vérification d'identité (MFA / Step-up Auth)
            self._verify_mfa_status()
            
            # COUCHE 3 : Autorisation stricte (RBAC / Ownership)
            self._check_permissions()
            
            # COUCHE 4 : Détection d'anomalies (Rate Limiting / Fraud detection)
            self._check_fraud_patterns()

            # COUCHE 5 : Protection de la donnée (Encryption / Integrity)
            return self._perform_secure_db_write()

        except SecurityException as e:
            # COUCHE 6 : Audit & Monitoring (On logue tout pour la détection)
            Logger.critical(f"Alerte Sécurité : {e.message} | User: {self.user.id}")
            raise

    def _validate_input(self):
        if not isinstance(self.data['amount'], (int, float)) or self.data['amount'] <= 0:
            raise SecurityException("Tentative d'injection ou montant invalide")

    def _verify_mfa_status(self):
        if not self.user.is_mfa_verified:
            raise SecurityException("Action sensible : MFA requis")

    def _check_permissions(self):
        # Vérification si le compte appartient bien à l'utilisateur (Anti-IDOR)
        if self.user.id != self.data['source_account_owner_id']:
            raise SecurityException("Tentative d'accès non autorisé à un compte tiers")