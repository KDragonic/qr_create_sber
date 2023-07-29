import base64
import logging
import random
import uuid
import requests

client_id = '2229344f-3622-417c-85e1-f57f75b1ae0b'
client_secret = '1a1a51fc-f7dc-4654-a12d-406f98b5519b'
cert_path = 'certificate_2229344f.pem'

auth_string = base64.b64encode((client_id + ':' + client_secret).encode()).decode()

def create_qr(access_token : str):

    # access_token = access_token.replace("-", "")

    url = "https://mc.api.sberbank.ru/prod/qr/order/v3/creation"

    client_id = '2229344f-3622-417c-85e1-f57f75b1ae0b'
    client_secret = '1a1a51fc-f7dc-4654-a12d-406f98b5519b'

    headers = {
        'Accept': '*/*',
        'Authorization': 'Basic ' + access_token,
        'Content-Type': 'application/json',
        'x-ibm-client-id': client_id,
        'x-ibm-client_secret': client_secret,
    }

    # https://mc.api.sberbank.ru/prod/order/v1

    member_id = random.randint(10000000, 99999999)

    param = {
        # "rq_uid": access_token,
        # "rq_tm": "2023-06-15T15:52:01Z",
        # "member_id": member_id,
        # "order_number": "774635526647",
        # "order_create_date": "2023-06-15T15:52:01Z",
        # "order_sum": 48000,
        # "currency": "643",
        # "description": "Water Still"
    }

    response = requests.post(url, data=param, headers=headers, verify=False, cert=cert_path)
    # response = requests.post(url, data=param, headers=headers, verify=False, cert=cert_path)

    json = response.json()

    content = {
        "status_code": response.status_code,
        "json": json,
    }

    return content


rquid = str(uuid.uuid4()).replace('-', '')

def get_access_token():
    url = 'https://mc.api.sberbank.ru:443/prod/tokens/v3/oauth'

    client_id = '2229344f-3622-417c-85e1-f57f75b1ae0b'
    client_secret = '1a1a51fc-f7dc-4654-a12d-406f98b5519b'

    auth_string = base64.b64encode((client_id + ':' + client_secret).encode()).decode()

    headers = {
        'accept': 'application/json',
        'authorization': 'Basic ' + auth_string,
        'content-type': 'application/x-www-form-urlencoded',
        'rquid': rquid
    }

    data = {
        'grant_type': 'client_credentials',
        'scope': 'https://api.sberbank.ru/qr/order.create'
    }

    response = requests.post(url, headers=headers, verify=False, data=data, cert=cert_path)

    if response.status_code != 200:
        print(f"Ошибка получения токена, код: {response.status_code}")
        print(response.text)
        return

    access_token = response.json().get('access_token')
    if not access_token:
        print("В ответе отсутствует access_token")

    return access_token

# print(content)

token = get_access_token()
create_qr(token)



