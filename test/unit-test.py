import pytest
from unittest.mock import patch, Mock
import requests
from azure_graph_toolkit.utils import decorators
from azure_graph_toolkit.graph_utils import (
    get_user_from_upn,
    get_user_membership_groups,
    get_user_group_by_name,
    add_user_to_group,
    remove_user_from_group
)

def run_generic_http_test(func_to_test, func_args, expected_info: dict, http_method: str, mock_response_json: dict = None, should_raise: bool = False):
    """
    Testa una funzione decorata con handle_http_exceptions che utilizza un metodo HTTP specifico.

    Args:
        func_to_test (callable): La funzione decorata da testare.
        func_args (tuple): Argomenti da passare alla funzione di test.
        expected_error_info (dict): Il dizionario con le informazioni di errore attese.
        http_method (str): Il metodo HTTP da testare ('get', 'post', 'patch', 'delete').
    """
    # test http exception
    if should_raise:
        # Mock della risposta HTTP e dell'eccezione
        mock_response = Mock()
        mock_response.status_code = expected_info["status_code"]
        mock_response.json.return_value = {
            "error": expected_info["error"],
            "error_description": expected_info["error_description"]
        }

        # Simulazione di eccezione HTTPError
        mock_http_error = requests.exceptions.HTTPError(response=mock_response)

        # metodo patch HTTP parametrizzato
        patch_target = f'requests.{http_method.lower()}'

        # Patch del metodo HTTP specificato per sollevare l'eccezione simulata
        with patch(patch_target, side_effect=mock_http_error):
            with pytest.raises(decorators.GraphHTTPError) as exc_info:
                func_to_test(*func_args)

            # Verifica che l'eccezione contenga le informazioni attese
            assert exc_info.value.args[0] == expected_info

    # test success response
    else:
        # Mock della risposta HTTP di successo
        mock_response = Mock()
        mock_response.status_code = 200

        if mock_response_json is not None:
            mock_response.json.return_value = mock_response_json

        # Determina quale metodo HTTP patchare
        patch_target = f'requests.{http_method.lower()}'

        # Patch del metodo HTTP specificato per restituire la risposta simulata
        with patch(patch_target, return_value=mock_response):
            result = func_to_test(*func_args)

            # Verifica che il risultato contenga le informazioni attese
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
        "error": "ResourceNotFound",
        "error_description": "The user was not found."
    }

    run_generic_http_test(get_user_from_upn, func_args, expected_error_info, 'get', mock_json_response, should_raise=True)

def test_success_get_user_from_upn():
    func_args = ("user@example.com", "fake_access_token")


    mock_json_response = {
        'id': 'user-id',
        'userPrincipalName': 'user@example.com',
        'jobTitle':'Developer'
    }

    # Definisci le informazioni attese per il caso di successo
    expected_success_info = {
        'status_code': 200,
        'id': 'user-id',
        'upn': 'user@example.com',
        'job_title': 'Developer'
    }

    # Esegui il test generico per il metodo GET, aspettandoti una risposta di successo
    run_generic_http_test(get_user_from_upn, func_args, expected_success_info, 'get', mock_json_response, should_raise=False)


def test_error_get_user_membership_groups():
    func_args = ("user@example.com", "fake_access_token")
    expected_error_info = {
        "status_code": 404,
        "error": "ResourceNotFound",
        "error_description": "No AAD groups found for user."
    }
    run_generic_http_test(get_user_membership_groups, func_args, expected_error_info, 'get', should_raise=True)        

def test_success_get_user_membership_groups():
    func_args = ('user@example.com','fake_access_token')
    mock_response_json = {'@odata.context': 'https://graph.microsoft.com/v1.0/$metadata#directoryObjects',
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
    func_args = ("user@example.com", "fake_group_name", "fake_access_token")
    expected_error_info = {
        "status_code": 404,
        "error": "ResourceNotFound",
        "error_description": "No AAD groups found for user."
    }
    run_generic_http_test(get_user_group_by_name, func_args, expected_error_info, 'get', should_raise=True)

def test_error_add_user_to_group():
    func_args = ("user@example.com", "fake_group_name", "fake_access_token")

    expected_error_info = {
        "status_code": 404,
        "error": "ResourceNotFound",
        "error_description": "No AAD groups found for user."
    }

    with patch('azure_graph_toolkit.graph_utils.get_user_from_upn') as mock_get_user_from_upn, \
         patch('azure_graph_toolkit.graph_utils.get_group_by_name') as mock_get_group_by_name, \
         patch('requests.post') as mock_post:

        # Configurazione dei mock per le chiamate GET come prerequisito della funzione add_user_to_group<
        mock_get_user_from_upn.return_value = {'id': 'user-id'}
        mock_get_group_by_name.return_value = {'group_id': 'group-id', 'group_name': 'fake_group_name'}

        # Simulazione di un errore nella chiamata POST
        mock_response_post = Mock()
        mock_response_post.status_code = 404
        mock_response_post.json.return_value = {
            "error": "ResourceNotFound",
            "error_description": "No AAD groups."
        }
        mock_post.side_effect = requests.exceptions.HTTPError(response=mock_response_post)


        run_generic_http_test(add_user_to_group, func_args, expected_error_info, 'post', should_raise=True)
