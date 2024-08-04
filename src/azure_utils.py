import requests
import json
import logging
import config
from app_auth import get_access_token


logging.basicConfig(level=logging.ERROR)

# TODO: da aggiungere in folder utils
def update_header(access_token):
    return{
        'Authorization': f'Bearer {access_token}',
        'Content-type': 'application/json',
        'ConsistencyLevel': 'eventual'
    }

def is_user_in_group():
    return

def get_user_from_upn (UPN, access_token ):

    url = f'{config.GRAPH_BASE_URL}/users/{UPN}' 

    headers = update_header(access_token)

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response_data = json.loads(response.text)

        user_id = response_data.get('id')
        upn= response_data.get('userPrincipalName')
        job = response_data.get('jobTitle')    

        return {
            'status_code': response.status_code,
            'id': user_id,
            'upn': upn,
            'job_title':job
        }
    except requests.exceptions.HTTPError as e:
        error_message = e.response.json().get('error', {}).get('message',str(e))
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

def get_user_group_by_name (user_id,group_name,access_token):

    url = f'{config.GRAPH_BASE_URL}/users/{user_id}/memberOf/microsoft.graph.group'

    params = {
        '$count': 'true',
        '$search': f'"displayName:{group_name}"',
        '$select': 'displayName,id'
    }

    header = update_header(access_token)

    try:
        result = requests.get(url,headers=header, params=params)
        result.raise_for_status()
        groups_data = result.json()

        for group in groups_data['value']:
            if group_name in group['displayName']:
                return {
                    'status_code':result.status_code,
                    'group_id':group['id'],
                    'group_name':group['displayName']
                }
        return {
            'status_code':result.status_code,
            'error':f'No AAD group that contains {group_name} for user {user_id} found. Try another name.'
        }
    except requests.exceptions.HTTPError as e: 
        error_message = e.response.json().get('error', {}).get('message',str(e))
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
    
def add_user_to_group(user_id, group_id, access_token):

    url = f'{config.GRAPH_BASE_URL}/groups/{group_id}/members/$ref'

    payload = {
        '@odata.id': f'{config.GRAPH_BASE_URL}/directoryObjects/{user_id}'
    }

    headers = update_header(access_token)
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        return {
            'status_code':response.status_code,
            'message': f'Success. User {user_id} added to AAD group {group_id}.'
        }
    
    except requests.exceptions.HTTPError as e:
        error_message = e.response.json().get('error', {}).get('message',str(e))
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

def remove_user_from_group(user_id, group_id, access_token):

    url = f'{config.GRAPH_BASE_URL}/groups/{group_id}/members/{user_id}/$ref'
    headers = update_header(access_token)
    try:
        
        response = requests.delete(url, headers=headers)
        response.raise_for_status()

        return {
            'status_code':response.status_code,
            'message': f'Success. User {user_id} removed from AAD group {group_id}.'
        }

    except requests.exceptions.HTTPError as e:
        error_message = e.response.json().get('error', {}).get('message',str(e))
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
