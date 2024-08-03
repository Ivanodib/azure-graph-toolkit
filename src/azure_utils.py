import requests
import json
import logging
import config
from app_auth import get_access_token




def get_user_id_from_upn (UPN, access_token ):

    url = f'{config.GRAPH_BASE_URL}/v1.0/users/{UPN}'  #?$select=id'

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

def get_user_group_by_name (user_id,group_name,access_token):

    url = f'{config.GRAPH_BASE_URL}/v1.0/users/{user_id}/memberOf/microsoft.graph.group'

    params = {
        '$count': 'true',
        '$search': f'"displayName:{group_name}"',
        '$select': 'displayName,id'
    }

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-type': 'application/json',
        'ConsistencyLevel': 'eventual'
    }

    try:
        result = requests.get(url,headers=headers, params=params)
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
    
def add_user_to_group(user_id, group_id, access_token):
    return


def remove_user_from_group(user_id, group_id, access_token):
    return