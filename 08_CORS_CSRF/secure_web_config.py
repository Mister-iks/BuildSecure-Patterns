from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

# 1. Configuration CORS : On bannit le "*" !
origins = [
    "https://mon-app-front.com",
    "https://admin.mon-app-front.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Seuls ces domaines peuvent nous parler
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["Authorization", "Content-Type"],
    allow_credentials=True, # Indispensable pour les cookies/auth
)

# 2. Protection CSRF (via les cookies SameSite)
# On configure les cookies pour qu'ils ne soient pas envoyés lors de requêtes cross-site
app.add_middleware(
    SessionMiddleware, 
    secret_key="SECRET_TRES_LONG_ET_SUR",
    https_only=True, # Uniquement via HTTPS
    same_site="lax" # Empêche l'envoi du cookie sur les requêtes de sites tiers
)

@app.post("/virement")
async def execute_transfer(amount: float):
    # En plus du SameSite, l'utilisation d'un Header custom (ex: X-Requested-With)
    # ou d'un Token CSRF spécifique est la règle d'or.
    return {"status": "Virement effectué en toute sécurité"}