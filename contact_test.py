import requests
from bs4 import BeautifulSoup

URL = "https://moneyexchange.ma/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

session = requests.Session()

print("=" * 70)
print("       TEST DU FORMULAIRE /contact")
print("=" * 70)

# --------------------------------------------------
# 1. Récupération de la page
# --------------------------------------------------

response = session.get(
    URL,
    headers=headers,
    timeout=15
)

print("\n[1] GET /")
print("Status :", response.status_code)

# --------------------------------------------------
# 2. Récupération du token CSRF
# --------------------------------------------------

soup = BeautifulSoup(response.text, "html.parser")

token = soup.find("input", {"name": "_token"})

if not token:
    print("[ERREUR] Token CSRF introuvable.")
    exit()

csrf_token = token.get("value")

print("[+] Token CSRF trouvé.")
print("[+] Valeur masquée pour sécurité.")

# --------------------------------------------------
# 3. Données de test
# --------------------------------------------------

data = {
    "_token": csrf_token,
    "fullname": "Security Test",
    "email": "security-test@example.com",
    "subject": "Test de sécurité",
    "description": "Test fonctionnel contrôle.",
}

# --------------------------------------------------
# 4. Envoi POST /contact
# --------------------------------------------------

print("\n[2] POST /contact")

post_response = session.post(
    "https://moneyexchange.ma/contact",
    data=data,
    headers=headers,
    timeout=15,
    allow_redirects=False
)

print("Status :", post_response.status_code)

print("\nHeaders de réponse :")

for name, value in post_response.headers.items():
    print(f"{name}: {value}")

# --------------------------------------------------
# 5. Redirection
# --------------------------------------------------

if post_response.is_redirect:
    print("\n[+] Redirection détectée.")
    print("Location :", post_response.headers.get("Location"))
else:
    print("\n[+] Aucune redirection directe.")

# --------------------------------------------------
# 6. Résumé
# --------------------------------------------------

print("\n" + "=" * 70)
print("TEST TERMINE")
print("=" * 70)