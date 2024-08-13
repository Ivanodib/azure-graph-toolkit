from . import config
import requests
import logging
from .utils import decorators
from pprint import pprint

@decorators.handle_http_exceptions
def get_access_token(tenant_id:str, client_id:str, client_secret:str):
    """
    Retrieves an access token using client credentials.

    Args:
        tenant_id (str): The tenant ID of the Azure AD.
        client_id (str): The client ID of the application.
        client_secret (str): The client secret of the application.

    Returns:
        str: The access token retrieved from the OAuth 2.0 token endpoint.

    Raises:
        requests.exceptions.HTTPError: If the HTTP request to obtain the token fails.
    """

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
    return response.json().get('access_token')

