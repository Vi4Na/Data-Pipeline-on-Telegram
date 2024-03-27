# API de BOTs do Telegram

from getpass import getpass

token = getpass()


import json

import requests

base_url = f'https://api.telegram.org/bot{token}'


response = requests.get(url=f'{base_url}/getMe')
print(f'{base_url}/getMe')

print(json.dumps(json.loads(response.text), indent=2))



response = requests.get(url=f'{base_url}/getUpdates')

print(json.dumps(json.loads(response.text), indent=2))