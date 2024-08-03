import requests
import json
import logging
from app_auth import get_access_token



def get_user_id_from_upn (UPN, access_token ):

    url = f'https://graph.microsoft.com/v1.0/users/{UPN}?$select=id'

    headers = {
        'Authorization':f'Bearer {access_token}',
        'Content-type':'application/json',
        'ConsistencyLevel':'eventual'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_data = json.loads(response.text)
        user_id = response_data.get('id')    

        return {
            'status_code': response.status_code,
            'user_id': user_id
        }
    except requests.exceptions.HTTPError as e:
        error_message = e.response.json().get('error', {}).get('message',str(e))
        logging.error(f'Error: {error_message}.')
        return {
            'status_code': e.response.status_code,
            'error':error_message
        }

