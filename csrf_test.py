import requests
from bs4 import BeautifulSoup

BASE_URL = "https://moneyexchange.ma"
CONTACT_URL = BASE_URL + "/contact"

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0 Security-Test"
}

print("=" * 70)
print("             TEST DE PROTECTION CSRF")
print("=" * 70)

# ---------------------------------------------------------
# 1. Récupération du formulaire
# ---------------------------------------------------------

print("\n[1] GET /")

response = session.get(
    BASE_URL + "/",
    headers=headers,
    timeout=15
)

print("Status :", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

token_input = soup.find("input", {"name": "_token"})

if not token_input:
    print("[!] Aucun token CSRF trouvé.")
    exit()

csrf_token = token_input.get("value")

print("[+] Token CSRF trouvé.")

# ---------------------------------------------------------
# Fonction pour envoyer un test
# ---------------------------------------------------------

def send_test(name, data):

    print("\n" + "-" * 70)
    print(name)
    print("-" * 70)

    response = session.post(
        CONTACT_URL,
        data=data,
        headers=headers,
        timeout=15,
        allow_redirects=False
    )

    print("Status :", response.status_code)

    location = response.headers.get("Location")

    if location:
        print("Location :", location)

    print("Cookies reçus :", list(response.cookies.keys()))

    return response


# ---------------------------------------------------------
# Données communes
# ---------------------------------------------------------

common_data = {
    "fullname": "CSRF Security Test",
    "email": "csrf-test@example.com",
    "subject": "Security test",
    "description": "Test CSRF autorisé."
}


# ---------------------------------------------------------
# TEST 1 : Token correct
# ---------------------------------------------------------

data_valid = {
    "_token": csrf_token,
    **common_data
}

send_test(
    "[TEST 1] Token CSRF VALIDE",
    data_valid
)


# ---------------------------------------------------------
# TEST 2 : Token absent
# ---------------------------------------------------------

data_missing = {
    **common_data
}

send_test(
    "[TEST 2] Token CSRF ABSENT",
    data_missing
)


# ---------------------------------------------------------
# TEST 3 : Token invalide
# ---------------------------------------------------------

data_invalid = {
    "_token": "FAUX_TOKEN_123456",
    **common_data
}

send_test(
    "[TEST 3] Token CSRF INVALIDE",
    data_invalid
)


print("\n" + "=" * 70)
print("TEST TERMINE")
print("=" * 70)