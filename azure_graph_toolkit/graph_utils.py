import requests
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
        dict: A dictionary containings the group id and group name.
    
    Raises:
        requests.exceptions.HTTPError: If the HTTP request to obtain group fails."""


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

    # status.code = 200. Exception decorator doesn't work here.
    if groups_data['@odata.count'] == 0:  
        return {
            'status_code':404,
            'message':f'No AAD group that contains {group_name} found. Try another name.'
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
def get_user_from_upn (user_upn:str, access_token:str ) -> dict:

    """
    Gets AAD user Id from User Principal Name (UPN).

    Args:
        user_upn (str): User principal name to find. 
        access_token (str): Graph API access token.

    Returns:
        dict: A dictionary containing status_code, id, job_title .

    Raises:
        requests.exceptions.HTTPError: If the HTTP request to obtain the user id fails."""


    url = f'{config.GRAPH_BASE_URL_USER}/{user_upn}' 

    headers = get_http_header(access_token)

    response = requests.get(url, headers=headers)

    response.raise_for_status()
    if response.status_code != 200:
        return response
    
    response_data = response.json()

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
def get_user_membership_groups(user_upn:str, access_token:str) -> dict:
    """
    Lists all AAD groups the user is a member of.

    Args:
        user_upn (str): The User Principal Name (UPN).
        access_token (str): The Graph API access token.

    Returns:
        dict: A dictionary containing all group names and group ids which user is member of.
    
    Raises:
        requests.exceptions.HTTPError: If the HTTP request to obtain groups fails.            
    """    

    url = f'{config.GRAPH_BASE_URL_USER}/{user_upn}/memberOf/microsoft.graph.group?$count=true&$select=displayName,id'
    header = get_http_header(access_token)

    result = requests.get(url,headers=header)
    result.raise_for_status()
    groups_data = result.json()

    if groups_data['@odata.count'] == 0:
        return {
            'status_code':404,
            'message': f'No AAD groups found for user {user_upn}.'
        }
    
    parsed_response = [{"displayName": group["displayName"], "id": group["id"]} for group in groups_data["value"]]

    return {'status_code': result.status_code,
            'groups': parsed_response}

@decorators.handle_http_exceptions
def is_user_member_of(user_upn:str, group_name:str, access_token:str) -> bool:
    """
    Check if user is member of specific AAD group.

    Args:
        user_upn (str): The User Principal Name (UPN).
        group_name (str): The group name to search. This could be substring of the group name.
        access_token (str): The Grah API access token.

    Returns:
        bool: A boolean value.
    
    Raises:
        requests.exceptions.HTTPError: If the HTTP request to obtain the user group fails."""
    
    response = get_user_membership_groups(user_upn, access_token)

    for group in response['groups']:
        if group_name in group['displayName']:
            return True
    return False

@decorators.handle_http_exceptions
def get_user_group_by_name (user_id:str,group_name:str,access_token:str) -> dict: 
    
    """
    Gets specific AAD user group membership.

    Args:
        user_id (str): AAD user Id. 
        group_name (str): The group name to search. This could be substring of the group name.
        access_token (str): The Grah API access token.

    Returns:
        dict: A dictionary containing status code, group id, group name .
        
    Raises:
        requests.exceptions.HTTPError: If the HTTP request to obtain group fails."""

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

    if groups_data['@odata.count'] == 0:
        
        return {
            'status_code':404,
            'message':f'No AAD group that contains {group_name} found. Try another name.'
        }

    for group in groups_data['value']:
        if group_name in group['displayName']:
            return {
                'status_code':result.status_code,
                'group_id':group['id'],
                'group_name':group['displayName']
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
        dict: A dictionary containing the status code, id, job_title .
        
    Raises:
        requests.exceptions.HTTPError: If the HTTP request to add user fails.    """

    response_user_info = get_user_from_upn(user_upn, access_token)
    if response_user_info.get('status_code') != 200:
        return response_user_info

    user_id = response_user_info.get('id')

 
    response_user_group = get_group_by_name(group_name,access_token)
    if response_user_group.get('status_code') != 200:
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
        'message': f'User {user_upn} added to AAD group {group_name} successfully.'
    }

@decorators.handle_http_exceptions
def remove_user_from_group(user_upn:str, group_name:str, access_token:str) -> dict:

    """
    Removes user from Azure AD group.

    Args:
        user_upn (str): The User principal name to find.
        group_name (str): The group to find. This could be a substring of the group name.  
        access_token (str): The Graph API access token.

    Returns:
        dict: A dictionary containing the status code and graph result  .
    
    Raises:
        requests.exceptions.HTTPError: If the HTTP request to remove user fails."""

    response_user_info = get_user_from_upn(user_upn, access_token)

    if response_user_info.get('status_code') != 200:
        return response_user_info
    user_id = response_user_info.get('id')

   
    #response_user_group = get_user_group_by_name(user_id,group_name,access_token)
    response_user_group = get_group_by_name(group_name,access_token)
    if response_user_group.get('status_code') != 200:
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


@decorators.handle_http_exceptions
def user_reset_password(user_upn:str, new_password:str, access_token:str, force_change_password_next_signin:bool = False):

    # User.ReadWrite.All api permission
    # User Administrator to App service principal.
    """
    Resets the user's password.

    Args:
        user_upn (str): The user's principal name (UPN).
        new_password (str): The new password to set for the user.
        access_token (str): The access token for the Graph API.
        force_change_password_next_signin (bool, optional): If True, the user will be required to change the password at the next sign-in. Defaults to False.

    Returns:
        dict: A dictionary containing the status code and a message indicating the result of the operation.

     Raises:
        requests.exceptions.HTTPError: If the HTTP request to update user password fails.            
    """

    url = f'{config.GRAPH_BASE_URL_USER}/{user_upn}'

    headers = get_http_header(access_token)


    payload = {
        'passwordProfile': {
            'forceChangePasswordNextSignIn': force_change_password_next_signin,
            'password': new_password
        }
    }

    response = requests.patch(url, headers=headers, json=payload)
    response.raise_for_status()

    return {
        'status_code':response.status_code,
        'message': f'Success. User {user_upn} password has been changed.'
    }


@decorators.handle_http_exceptions
def user_revoke_sessions(user_upn:str, access_token: str):
    """
    Revokes all active sessions for a specified user.

    Args:
        user_upn (str): The user's principal name (UPN).
        access_token (str): The access token for the Graph API.

    Returns:
        dict: A dictionary containing the status code and a message indicating that the user's sessions were revoked.

    Raises:
        requests.exceptions.HTTPError: If the HTTP request to revoke sessions fails.
    """

    url = f'{config.GRAPH_BASE_URL_USER}/{user_upn}/revokeSignInSessions'
    headers = get_http_header(access_token)

    response = requests.post(url, headers=headers)
    response.raise_for_status()

    return {
        'status_code': response.status_code,
        'message': f'User {user_upn} sessions have been revoked successfully.'
    }

@decorators.handle_http_exceptions
def user_set_account_status(user_upn:str, enable_account:bool , access_token: str,) -> dict:

    """
    Sets the user's account status (enabled or disabled).

    Args:
        user_upn (str): The user's principal name.
        enable_account (bool): True to enable the account, False to disable it.
        access_token (str): The access token for the Graph API.

    Returns:
        dict: A dictionary containing the status code and the result of the operation.
    
    Raises:
        requests.exceptions.HTTPError: If the HTTP request to set account status fails.
    """

    url = f'{config.GRAPH_BASE_URL_USER}/{user_upn}'
    headers = get_http_header(access_token)

    payload = {
        'accountEnabled':enable_account
    }

    response = requests.patch(url, headers=headers, json=payload)
    response.raise_for_status()

    status_message = "enabled" if enable_account else "disabled"

    return {
        'status_code':response.status_code,
        'message': f'User account {user_upn} has been {status_message} successfully.'
    }

