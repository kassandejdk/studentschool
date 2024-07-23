
import requests
from django.conf import settings

def get_api_data(endpoint, params=None):
    url = f"{settings.API_BASE_URL}/{endpoint}"
    headers = {
        'Authorization': f'Bearer {settings.LigdiCash_API_Key}',
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
