from msal import ConfidentialClientApplication
from msal import SerializableTokenCache
import config
import os


def load_cache():
    cache = SerializableTokenCache()
    if os.path.exists('token_cache.json'):
        cache.deserialize(open('token_cache.json', 'r').read())
    return cache

def save_cache(cache):
    if cache.has_state_changed:
        open('token_cache.json', 'w').write(cache.serialize())



def get_access_token(tenant_id, client_id, client_secret):

    auth_url = f'{config.AUTH_BASE_URL}/{tenant_id}'
    scopes = ['https://graph.microsoft.com/.default']

    cache = load_cache()

    app = ConfidentialClientApplication(

        client_id=client_id,
        client_credential=client_secret,
        authority=auth_url,
        token_cache=cache
    )

    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(scopes, account=accounts[0])
    else:
        result = app.acquire_token_for_client(scopes=scopes)

    save_cache(cache)

    if 'access_token' in result:
        access_token = result.get('access_token')
    else:
        raise Exception("Could not obtain access token")

    return access_token

    
