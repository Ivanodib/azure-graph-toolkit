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

def run_generic_http_test(func_to_test, func_args, expected_error_info, http_method):
    """
    Testa una funzione decorata con handle_http_exceptions che utilizza un metodo HTTP specifico.

    Args:
        func_to_test (callable): La funzione decorata da testare.
        func_args (tuple): Argomenti da passare alla funzione di test.
        expected_error_info (dict): Il dizionario con le informazioni di errore attese.
        http_method (str): Il metodo HTTP da testare ('get', 'post', 'patch', 'delete').
    """
    # Mock della risposta HTTP e dell'eccezione
    mock_response = Mock()
    mock_response.status_code = expected_error_info["status_code"]
    mock_response.json.return_value = {
        "error": expected_error_info["error"],
        "error_description": expected_error_info["error_description"]
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
        assert exc_info.value.args[0] == expected_error_info
    

def test_error_get_user_from_upn():
    func_args = ("user@example.com", "fake_access_token")
    expected_error_info = {
        "status_code": 404,
        "error": "ResourceNotFound",
        "error_description": "The user was not found."
    }
    run_generic_http_test(get_user_from_upn, func_args, expected_error_info, 'get')

def test_error_get_user_membership_groups():
    func_args = ("user@example.com", "fake_access_token")
    expected_error_info = {
        "status_code": 404,
        "error": "ResourceNotFound",
        "error_description": "No AAD groups found for user."
    }
    run_generic_http_test(get_user_membership_groups, func_args, expected_error_info, 'get')        

def test_error_get_user_group_by_name():
    func_args = ("user@example.com", "fake_group_name", "fake_access_token")
    expected_error_info = {
        "status_code": 404,
        "error": "ResourceNotFound",
        "error_description": "No AAD groups found for user."
    }
    run_generic_http_test(get_user_group_by_name, func_args, expected_error_info, 'get')

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


        run_generic_http_test(add_user_to_group, func_args, expected_error_info, 'post')
