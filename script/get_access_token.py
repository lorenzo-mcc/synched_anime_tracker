import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_access_token():
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    token_url = "https://anilist.co/api/v2/oauth/token"

    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }

    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        print("Access token ottenuto:", access_token)
        return access_token
    else:
        print("Errore:", response.status_code, response.text)
        return None

if __name__ == "__main__":
    get_access_token()