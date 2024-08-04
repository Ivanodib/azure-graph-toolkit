import requests
import json
import logging
import config
from app_auth import get_access_token


logging.basicConfig(level=logging.ERROR)

# TODO: da aggiungere in folder utils
def get_http_header(access_token):

    return{
        'Authorization': f'Bearer {access_token}',
        'Content-type': 'application/json',
        'ConsistencyLevel': 'eventual'
    }

def is_user_in_group():
    return

def get_group_by_name(group_name, access_token):

    url = f'{config.GRAPH_BASE_URL}/groups/'

    params = {
        '$count': 'true',
        '$search': f'"displayName:{group_name}"',
        '$select': 'displayName,id'
    }

    header = get_http_header(access_token)

    try:
        respone_group_info = requests.get(url,headers=header, params=params)
        respone_group_info.raise_for_status()
        groups_data = respone_group_info.json()

        # Nessun gruppo trovato
        if groups_data['@odata.count'] == 0:  
            return {
                'status_code':respone_group_info.status_code,
                'error':f'No AAD group that contains {group_name} found. Try another name.'
            }
        
        else:
            count_match_name = 0
            data = {}
            for group in groups_data['value']:
                if group_name in group['displayName']:
                    count_match_name = count_match_name + 1
                    data = {
                        'status_code':respone_group_info.status_code,
                        'group_id':group['id'],
                        'group_name':group['displayName']
                    }
            # Diversi gruppi che contengono la substring
            if count_match_name > 1:
                return {
                    'status_code': respone_group_info.status_code,
                    'error':f'Too much AAD group that contains {group_name} found. Try another name.'
                }
            
            # Singolo gruppo AAD trovato
            elif count_match_name == 1:
                return data
            else:
                return {
                'status_code': respone_group_info.status_code,
                'error':f'No AAD group that contains {group_name} found. Try another name.'
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

def get_user_from_upn (UPN, access_token ):

    url = f'{config.GRAPH_BASE_URL}/users/{UPN}' 

    headers = get_http_header(access_token)

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

    header = get_http_header(access_token)

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
    
def add_user_to_group(user_upn, group_name, access_token):

    # Get user Id from UPN
    response_user_info = get_user_from_upn(user_upn, access_token)

    if 'error' in response_user_info:
        return response_user_info    
    user_id = response_user_info.get('id')

    # Find AAD group by name   
    response_user_group = get_group_by_name(group_name,access_token)

    if 'error' in response_user_group:
        return response_user_group
    
    group_id = response_user_group.get('group_id')
    group_name = response_user_group.get('group_name')



    url = f'{config.GRAPH_BASE_URL}/groups/{group_id}/members/$ref'

    payload = {
        '@odata.id': f'{config.GRAPH_BASE_URL}/directoryObjects/{user_id}'
    }

    headers = get_http_header(access_token)
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        return {
            'status_code':response.status_code,
            'message': f'Success. User {user_upn} added to AAD group {group_name}.'
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

def remove_user_from_group(user_upn, group_name, access_token):

    response_user_info = get_user_from_upn(user_upn, access_token)

    if 'error' in response_user_info:
        return response_user_info    
    user_id = response_user_info.get('id')

    # Find user membership by group name    
    response_user_group = get_user_group_by_name(user_id,group_name,access_token)

    if 'error' in response_user_group:
        return response_user_group
    
    group_id = response_user_group.get('group_id')
    group_name = response_user_group.get('group_name')

    url = f'{config.GRAPH_BASE_URL}/groups/{group_id}/members/{user_id}/$ref'
    headers = get_http_header(access_token)
    try:
        
        response = requests.delete(url, headers=headers)
        response.raise_for_status()

        return {
            'status_code':response.status_code,
            'message': f'Success. User {user_upn} removed from AAD group {group_name}.'
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
