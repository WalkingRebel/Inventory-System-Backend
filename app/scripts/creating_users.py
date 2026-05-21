import httpx

BASE_URL = "http://127.0.0.1:8000"

ADMIN_EMAIL = "admin@admin.com"
ADMIN_PASSWORD = "admin123"

USERS = [
    {"name": "Purchase User 1", "email": "purchase1@example.com", "password": "Passw0rd1!", "role_id": 2},
    {"name": "Purchase User 2", "email": "purchase2@example.com", "password": "Passw0rd2!", "role_id": 2},
    {"name": "Sales User 1", "email": "sales1@example.com", "password": "Passw0rd3!", "role_id": 3},
    {"name": "Sales User 2", "email": "sales2@example.com", "password": "Passw0rd4!", "role_id": 3},
    {"name": "Customer User 1", "email": "customer1@example.com", "password": "Passw0rd5!", "role_id": 4},
    {"name": "Customer User 2", "email": "customer2@example.com", "password": "Passw0rd6!", "role_id": 4},
    {"name": "Vendor User 1", "email": "vendor1@example.com", "password": "Passw0rd7!", "role_id": 5},
    {"name": "Vendor User 2", "email": "vendor2@example.com", "password": "Passw0rd8!", "role_id": 5},
    {"name": "Purchase User 3", "email": "purchase3@example.com", "password": "Passw0rd9!", "role_id": 2},
    {"name": "Sales User 3", "email": "sales3@example.com", "password": "Passw0rd10!", "role_id": 3},
]

def main() -> None:
    with httpx.Client(timeout=30) as client:
        # OAuth2PasswordRequestForm expects form fields: username, password
        login_resp = client.post(
            f"{BASE_URL}/api/v1/auth/login",
            data={"username": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
        )
        login_resp.raise_for_status()
        token = login_resp.json()["access_token"]

        headers = {"Authorization": f"Bearer {token}"}

        for u in USERS:
            resp = client.post(f"{BASE_URL}/api/v1/users/", json=u, headers=headers)
            if resp.status_code == 400 and "already exists" in resp.text.lower():
                print(f"SKIP {u['email']} (already exists)")
                continue
            resp.raise_for_status()
            created = resp.json()
            print(f"OK   {created['id']} {created['email']} role_id={created.get('role_id')}")

if __name__ == "__main__":
    main()