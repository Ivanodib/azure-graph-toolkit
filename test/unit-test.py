
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import patch, MagicMock
import pytest
import requests

from azure_graph_toolkit.graph_utils import (
    get_group_by_name,
    get_user_from_upn,
    decorators
)

class TestGetUserFromUpn:
    
    @patch('requests.get')
    def test_get_user_from_upn_success(self, mock_get):

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 'user123',
            'userPrincipalName': 'user@example.com',
            'jobTitle': 'Developer'
        }
        mock_get.return_value = mock_response
        

        result = get_user_from_upn('user@example.com', 'fake_token')
        assert result == {
            'status_code': 200,
            'id': 'user123',
            'upn': 'user@example.com',
            'job_title': 'Developer'
        }

    @patch('requests.get')
    def test_get_user_from_upn_http_error(self, mock_get):
        # Simula una risposta con errore HTTP
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
        'error': {
            'code': 'Request_ResourceNotFound',
            'message': "Resource 'user.example@domain.com' does not exist or one of its queried reference-property objects are not present.",
            'innerError': {
                'date': '2024-08-11T13:10:10',
                'request-id': 'request-id123',
                'client-request-id': 'client-request-id123'
            }
        },
        'error_description': None
    }
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)

        with patch('requests.get', return_value=mock_response):
            with pytest.raises(decorators.GraphHTTPError) as excinfo:
                get_user_from_upn('user@example.com', 'fake_token')
    
        # Verifica che l'eccezione sollevata contenga i dati corretti
        assert excinfo.value.args[0] == {
        'status_code':404,
        'error': {
            'code': 'Request_ResourceNotFound',
            'message': "Resource 'user.example@domain.com' does not exist or one of its queried reference-property objects are not present.",
            'innerError': {
                'date': '2024-08-11T13:10:10',
                'request-id': 'request-id123',
                'client-request-id': 'client-request-id123'
            }
        },
        'error_description': None
    }