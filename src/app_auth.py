from msal import ConfidentialClientApplication
import requests

def get_access_token(tenant_id, client_id, client_secret):

    auth_url = f'https://login.microsoftonline.com/{tenant_id}'
    scopes = ['https://graph.microsoft.com/.default']

    app = ConfidentialClientApplication(

        client_id=client_id,
        client_credential=client_secret,
        authority=auth_url
    )

    respone = app.acquire_token_for_client(scopes=scopes)
    access_token = respone.get('access_token')

    return access_token
    
