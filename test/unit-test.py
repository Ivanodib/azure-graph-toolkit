import pytest
from unittest.mock import patch, Mock
import requests
from azure_graph_toolkit.utils import decorators
from azure_graph_toolkit.graph_utils import (
    get_user_from_upn,
    get_user_membership_groups,
    get_user_group_by_name,
    add_user_to_group,
    remove_user_from_group,
    user_revoke_sessions,
    user_set_account_status
)

def run_generic_http_test(func_to_test, func_args, expected_info: dict, http_method: str, mock_response_json: dict = None, should_raise: bool = False):

    """
    Runs a generic HTTP test for a function decorated with handle_http_exceptions.

    Args:
        func_to_test (callable): The decorated function to be tested.
        func_args (tuple): Arguments to pass to the function being tested.
        expected_info (dict): A dictionary with the expected information or error details.
        http_method (str): The HTTP method to be tested ('get', 'post', 'patch', 'delete').
        mock_response_json (dict, optional): A dictionary representing the JSON response to be returned by the mock. Defaults to None.
        should_raise (bool, optional): If True, the test will simulate an HTTP error and expect an exception. Defaults to False.

    Returns:
        None: The function asserts the test results and does not return anything.

    Raises:
        AssertionError: If the actual result does not match the expected information.
    """

    mock_response = Mock()
    mock_response.json.return_value = mock_response_json
    patch_target = f'requests.{http_method.lower()}'

    # test http exception
    if should_raise:

        mock_response.status_code = expected_info['status_code']
        mock_http_error = requests.exceptions.HTTPError(response=mock_response)

        with patch(patch_target, side_effect=mock_http_error):
            result = func_to_test(*func_args)
            

    # test success response
    else:
        mock_response.status_code = 200

        with patch(patch_target, return_value=mock_response):
            result = func_to_test(*func_args)

    assert result == expected_info

def test_error_get_user_from_upn():
    func_args = ("user@example.com", "fake_access_token")
    
    mock_json_response = {
        'status_code': 404,
        'error': 
        {
        'code': 'Request_ResourceNotFound',
        'message': "Resource 'user@example.com' does not exist or one of its queried reference-property objects are not present.",
        'innerError':
          {
            'date': '2024-08-12T14:29:59',
            'request-id': 'xxxxxxxxxxxxxxxxxxxxxx',
            'client-request-id': 'yyyyyyyyyyyyyyyy'
            }
            },
            'error_description': None}
    
    
    expected_error_info = {
        "status_code": 404,
        "message": "Resource 'user@example.com' does not exist or one of its queried reference-property objects are not present."
    }

    run_generic_http_test(get_user_from_upn, func_args, expected_error_info, 'get', mock_json_response, should_raise=True)

def test_success_get_user_from_upn():
    func_args = ("user@example.com", "fake_access_token")


    mock_json_response = {
        'id': 'user-id',
        'userPrincipalName': 'user@example.com',
        'jobTitle':'Developer'
    }

    expected_success_info = {
        'status_code': 200,
        'id': 'user-id',
        'upn': 'user@example.com',
        'job_title': 'Developer'
    }

    run_generic_http_test(get_user_from_upn, func_args, expected_success_info, 'get', mock_json_response, should_raise=False)

def test_error_get_user_membership_groups():
    mock_user_upn = "user@example.com"
    
    func_args = (mock_user_upn, "fake_access_token")

    expected_error_info = {
        "status_code": 404,
        "message":f"No AAD groups found for user {mock_user_upn}."
    }

    mock_json_response = {
        '@odata.count': 0
    }
    
    run_generic_http_test(get_user_membership_groups, func_args, expected_error_info, 'get', mock_json_response, should_raise=False)        

def test_success_get_user_membership_groups():
    func_args = ('user@example.com','fake_access_token')
    mock_response_json = {'@odata.context': 'https://graph.microsoft.com/v1.0/$metadata#directoryObjects',
                          '@odata.count':2,
                 'value': [
                        {'@odata.type': '#microsoft.graph.group',
                            'id': 'xxxxxxxxxxxxxxxx',
                            'createdDateTime': '2003-05-12T14:00:03Z',
                            'creationOptions': [],
                            'description': None,
                            'displayName': 'Group-A',
                            'expirationDateTime': None },
                        {'@odata.type': '#microsoft.graph.group',
                            'id': 'yyyyyyyyyyyyyyyy',
                            'createdDateTime': '2003-05-12T14:00:00Z',
                            'creationOptions': [],
                            'description': None,
                            'displayName': 'Group-B',
                            'expirationDateTime': None }]}

    expected_info = {
        'status_code': 200,
        'groups': [
            {'displayName': 'Group-A', 'id': 'xxxxxxxxxxxxxxxx'},
            {'displayName': 'Group-B', 'id': 'yyyyyyyyyyyyyyyy'}]
            }
    run_generic_http_test(get_user_membership_groups,func_args,expected_info,'get',mock_response_json,should_raise=False)

def test_error_get_user_group_by_name():

    mock_group_name = 'Group-A'
    func_args = ("fake_user_id", mock_group_name, "fake_access_token")
    expected_error_info = {
            'status_code':404,
            'message':f'No AAD group that contains {mock_group_name} found. Try another name.'
        }
    
    mock_json_response = {
        '@odata.count': 0
    }

    run_generic_http_test(get_user_group_by_name, func_args, expected_error_info, 'get', mock_json_response,should_raise=False)

def test_success_get_user_group_by_name():
    func_args = ('user-id','Group-A','fake_access_token')
    expected_info = {
        'status_code':200,
        'group_id':'xxxxxxx',
        'group_name':'Group-A'
    }

    mock_json_response = {
        '@odata.context': 'https://graph.microsoft.com/v1.0/$metadata#groups(displayName,id)',
            '@odata.count': 1, 'value':[{
            'displayName': 'Group-A',
            'id': 'xxxxxxx'}]
            }
    
    run_generic_http_test(get_user_group_by_name,func_args,expected_info,'get',mock_json_response,should_raise=False)

def test_error_add_user_to_group():

    mock_user_id = "user-id"
    mock_group_name = "Group-A"
    
    func_args = ("user@example.com", mock_group_name, "fake_access_token")

    expected_error_info = {
        "status_code": 400,
        "message":"One or more added object references already exist for the following modified properties: 'members'."
    }

    mock_json_response = {
        'error': {'code': 'Request_BadRequest', 'message': "One or more added object references already exist for the following modified properties: 'members'.",
        'innerError': {'date': '2024-08-21T23:23:06', 'request-id': 'ef95f7c5-17e5-49de-bac2-bf68f6a622c0', 'client-request-id': 'ef95f7c5-17e5-49de-bac2-bf68f6a622c0'}}
        }
    

    with patch('azure_graph_toolkit.graph_utils.get_user_from_upn') as mock_get_user_from_upn, \
         patch('azure_graph_toolkit.graph_utils.get_group_by_name') as mock_get_group_by_name:
   
        mock_get_user_from_upn.return_value = {'status_code':200, 'id': mock_user_id}
        mock_get_group_by_name.return_value = {'status_code':200, 'group_id': 'group-id', 'group_name': mock_group_name}

        run_generic_http_test(add_user_to_group, func_args, expected_error_info, 'post', mock_json_response , should_raise=True)

def test_success_add_user_to_group():
    
    mock_user_upn = "user@example.com"
    mock_group_name = "Group-A"
    
    func_args = (mock_user_upn, mock_group_name, "fake_access_token")

    with patch('azure_graph_toolkit.graph_utils.get_user_from_upn') as mock_get_user_from_upn, \
        patch('azure_graph_toolkit.graph_utils.get_group_by_name') as mock_get_group_by_name:

        mock_get_user_from_upn.return_value = {'status_code':200, 'id': 'user-id'}
        mock_get_group_by_name.return_value = {'status_code':200, 'group_id': 'group-id', 'group_name': mock_group_name}

        expected_info = {
        'status_code':200,
        'message': f'User {mock_user_upn} added to AAD group {mock_group_name} successfully.'
        }

        mock_json_response = {
        'status_code':200
        }

        run_generic_http_test(add_user_to_group,func_args,expected_info,'post',mock_json_response, should_raise=False)

def test_error_remove_user_from_group():

    mock_group_name = 'Group-A'
    mock_user_id = 'user-id'
    func_args = ('user@example.com','Group-A','fake_access_token')


    with patch('azure_graph_toolkit.graph_utils.get_user_from_upn') as mock_get_user_from_upn, \
        patch('azure_graph_toolkit.graph_utils.get_group_by_name') as mock_get_group_by_name:

        mock_get_user_from_upn.return_value = {'status_code':200, 'id': mock_user_id}
        mock_get_group_by_name.return_value = {'status_code':200, 'group_id': 'group-id', 'group_name': mock_group_name}


        expected_error_info = {
        'status_code': 404,
        'message': "Resource '29420684-fee0-49e1-b9c5-dbdefd57c48f' does not exist or one of its queried reference-property objects are not present."
        }


        mock_json_response = {
        'error': {'code': 'Request_ResourceNotFound',
        'message': "Resource '29420684-fee0-49e1-b9c5-dbdefd57c48f' does not exist or one of its queried reference-property objects are not present.",
        'innerError': {'date': '2010-08-21T00:00:00', 'request-id': 'xxxxxxxxxx', 'client-request-id': 'yyyyyyyyyyyy'}}
        }

        run_generic_http_test(remove_user_from_group, func_args, expected_error_info, 'delete', mock_json_response , should_raise=True)

def test_success_user_revoke_sessions():
    mock_user_upn = "user@example.com"
    
    func_args = (mock_user_upn,  "fake_access_token")

    expected_info = {
        'status_code': 200,
        'message': f'User {mock_user_upn} sessions have been revoked successfully.'
    }

    mock_json_response = {
        "@odata.context": "https://graph.microsoft.com/v1.0/$metadata#Edm.Boolean",
        "value": True
    }

    run_generic_http_test(user_revoke_sessions, func_args, expected_info,'post', mock_json_response, should_raise=False)


def test_success_user_set_account_status():
    mock_user_upn = "user@example.com"
    enable_account = True
    
    func_args = (mock_user_upn, enable_account,  "fake_access_token")

    expected_info = {
        'status_code': 200,
        'message': f'User account {mock_user_upn} has been enabled successfully.'
    }

    mock_json_response = {
        
    }

    run_generic_http_test(user_set_account_status, func_args, expected_info,'patch', mock_json_response, should_raise=False)
