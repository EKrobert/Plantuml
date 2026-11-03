import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://moneyexchange.ma/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

print("=" * 70)
print("        ANALYSE DES REQUETES HTTP")
print("=" * 70)

try:
    session = requests.Session()

    response = session.get(
        URL,
        headers=headers,
        timeout=15
    )

    print("\n[+] Requete principale")
    print("Method :", response.request.method)
    print("URL    :", response.url)
    print("Status :", response.status_code)

    print("\n[+] Headers envoyes")
    for name, value in response.request.headers.items():
        print(f"{name}: {value}")

    print("\n[+] Headers recus")
    for name, value in response.headers.items():
        print(f"{name}: {value}")

    print("\n[+] Cookies recus")

    for cookie in session.cookies:
        # On affiche uniquement le nom, jamais la valeur
        print(f"- {cookie.name}")

    # Analyse HTML
    soup = BeautifulSoup(response.text, "html.parser")

    print("\n" + "=" * 70)
    print("FORMULAIRES")
    print("=" * 70)

    forms = soup.find_all("form")

    if not forms:
        print("[+] Aucun formulaire trouve.")
    else:

        for number, form in enumerate(forms, start=1):

            action = form.get("action", "")
            method = form.get("method", "GET").upper()

            action_url = urljoin(response.url, action)

            print(f"\n--- Formulaire {number} ---")
            print("Method :", method)
            print("Action :", action_url)

            fields = form.find_all(["input", "textarea", "select", "button"])

            if fields:
                print("\nChamps :")

                for field in fields:

                    tag = field.name
                    name = field.get("name", "")
                    field_type = field.get("type", "")

                    print(
                        f"  {tag:<10} "
                        f"name={name!r:<25} "
                        f"type={field_type!r}"
                    )

            else:
                print("Aucun champ.")

    print("\n" + "=" * 70)
    print("LIENS / ENDPOINTS")
    print("=" * 70)

    links = soup.find_all("a")

    found = set()

    for link in links:

        href = link.get("href")

        if not href:
            continue

        full_url = urljoin(response.url, href)

        if full_url not in found:
            found.add(full_url)
            print(full_url)

    print("\n" + "=" * 70)
    print("ANALYSE TERMINEE")
    print("=" * 70)

except requests.exceptions.RequestException as e:

    print("\n[ERREUR]")
    print(e)