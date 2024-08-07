import requests
import json
import logging
from . import config
from .utils import decorators

logging.basicConfig(level=logging.ERROR)

def get_http_header(access_token:str) -> dict:

    """
    Return common http header with access token updated.

    Args:
        access_token (str): Graph API access token.

    Returns:
        dict: A dictionary containing the HTTP header with new access token."""

    return{
        'Authorization': f'Bearer {access_token}',
        'Content-type': 'application/json',
        'ConsistencyLevel': 'eventual'
    }


@decorators.handle_http_exceptions
def get_group_by_name(group_name:str, access_token:str) -> dict :
    
    """
    Gets Azure AD group information by name.

    Args:
        group_name (str): The group name to find. This could be a substring of the group name. 
        access_token (str): The Graph API access token.

    Returns:
        dict: A dictionary containings the group id and group name."""


    url = f'{config.GRAPH_BASE_URL_GROUP}/'

    params = {
        '$count': 'true',
        '$search': f'"displayName:{group_name}"',
        '$select': 'displayName,id'
    }

    header = get_http_header(access_token)

    respone_group_info = requests.get(url,headers=header, params=params)
    respone_group_info.raise_for_status()
    groups_data = respone_group_info.json()

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
        
        if count_match_name > 1:
            return {
                'status_code': respone_group_info.status_code,
                'error':f'Too much AAD group that contains {group_name} found. Try another name.'
            }
        

        elif count_match_name == 1:
            return data
        else:
            return {
            'status_code': respone_group_info.status_code,
            'error':f'No AAD group that contains {group_name} found. Try another name.'
        }


@decorators.handle_http_exceptions
def get_user_from_upn (UPN:str, access_token:str ) -> dict:

    """
    Gets AAD user Id from User Principal Name (UPN).

    Args:
        user_upn (str): User principal name to find. 
        access_token (str): Graph API access token.

    Returns:
        dict: A dictionary containing status_code, id, job_title ."""


    url = f'{config.GRAPH_BASE_URL_USER}/{UPN}' 

    headers = get_http_header(access_token)

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


@decorators.handle_http_exceptions
def get_user_group_by_name (user_id:str,group_name:str,access_token:str) -> dict: 
    
    """
    Gets AAD user group membership.

    Args:
        user_id (str): AAD user Id. 
        group_name (str): The group name to search. This could be substring of the group name.
        access_token (str): The Grah API access token.

    Returns:
        dict: A dictionary containing status code, group id, group name ."""

    url = f'{config.GRAPH_BASE_URL_USER}/{user_id}/memberOf/microsoft.graph.group'

    params = {
        '$count': 'true',
        '$search': f'"displayName:{group_name}"',
        '$select': 'displayName,id'
    }

    header = get_http_header(access_token)

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


@decorators.handle_http_exceptions    
def add_user_to_group(user_upn:str, group_name:str, access_token:str) -> dict:

    """
    Adds user to Azure AD group.

    Args:
        user_upn (str): The User principal name to find.
        group_name (str): The group to find. This could be a substring of the group name.  
        access_token (str): The Graph API access token.

    Returns:
        dict: A dictionary containing the status code, id, job_title ."""

    response_user_info = get_user_from_upn(user_upn, access_token)

    if 'error' in response_user_info:
        return response_user_info    
    user_id = response_user_info.get('id')

 
    response_user_group = get_group_by_name(group_name,access_token)

    if 'error' in response_user_group:
        return response_user_group
    
    group_id = response_user_group.get('group_id')
    group_name = response_user_group.get('group_name')


    url = f'{config.GRAPH_BASE_URL_GROUP}/{group_id}/members/$ref'
    payload = {
        '@odata.id': f'{config.GRAPH_BASE_URL}/directoryObjects/{user_id}'
    }

    headers = get_http_header(access_token)
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    return {
        'status_code':response.status_code,
        'message': f'Success. User {user_upn} added to AAD group {group_name}.'
    }


@decorators.handle_http_exceptions
def remove_user_from_group(user_upn:str, group_name:str, access_token:str) -> dict:

    """
    Adds user to Azure AD group.

    Args:
        user_upn (str): The User principal name to find.
        group_name (str): The group to find. This could be a substring of the group name.  
        access_token (str): The Graph API access token.

    Returns:
        dict: A dictionary containing the status code and graph result  ."""

    response_user_info = get_user_from_upn(user_upn, access_token)

    if 'error' in response_user_info:
        return response_user_info    
    user_id = response_user_info.get('id')
   
    response_user_group = get_user_group_by_name(user_id,group_name,access_token)

    if 'error' in response_user_group:
        return response_user_group
    
    group_id = response_user_group.get('group_id')
    group_name = response_user_group.get('group_name')

    url = f'{config.GRAPH_BASE_URL_GROUP}/{group_id}/members/{user_id}/$ref'
    headers = get_http_header(access_token)
        
    response = requests.delete(url, headers=headers)
    response.raise_for_status()

    return {
        'status_code':response.status_code,
        'message': f'Success. User {user_upn} removed from AAD group {group_name}.'
    }
  