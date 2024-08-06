from . import config
import requests
import logging

def get_access_token(tenant_id, client_id, client_secret):

    auth_url = f'{config.AUTH_BASE_URL}/{tenant_id}/oauth2/v2.0/token'
    scope = {config.GRAPH_SCOPE}

    header = {
        'Content-type': 'application/x-www-form-urlencoded'
    }

    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials',
        'scope': scope
    }

    try:
        response = requests.post(auth_url,headers=header, data=data)
        response.raise_for_status()
        token = response.json()["access_token"]
        return token

    except requests.exceptions.HTTPError as e:
        error_message = e.response.text
        logging.error(f'Error: {error_message}.')
        return {
            'status_code': e.response.status_code,
            'error':error_message
        }
    except requests.exceptions.RequestException as e:
        logging.error(f'Request failed: {e}')
        return {
            'status_code': None,
            'error': str(e)
        } 
    
