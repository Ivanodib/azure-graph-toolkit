from msal import ConfidentialClientApplication
import config
import os


def get_access_token(tenant_id, client_id, client_secret):

    auth_url = f'{config.AUTH_BASE_URL}/{tenant_id}'
    scopes = ['https://graph.microsoft.com/.default']

    app = ConfidentialClientApplication(

        client_id=client_id,
        client_credential=client_secret,
        authority=auth_url
    )
    
    result = app.acquire_token_for_client(scopes=scopes)
    return result.get('access_token')



    
