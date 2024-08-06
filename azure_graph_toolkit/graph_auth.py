from . import config
import requests
import logging
from .utils import decorators

@decorators.handle_http_exceptions
def get_access_token(tenant_id:str, client_id:str, client_secret:str):

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

    response = requests.post(auth_url,headers=header, data=data)
    response.raise_for_status()
    token = response.json()["access_token"]
    return token
