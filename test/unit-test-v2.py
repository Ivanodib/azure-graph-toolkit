import pytest
from unittest.mock import patch
import requests
from azure_graph_toolkit.graph_utils import (
    decorators,
    get_group_by_name, get_user_from_upn, get_user_membership_groups, 
    if_user_member_of, get_user_group_by_name, add_user_to_group, 
    remove_user_from_group, user_reset_password, user_revoke_sessions
)

# Esempio di fixture per mocking delle risposte API
@pytest.fixture
def mock_response(monkeypatch):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def raise_for_status(self):
            if self.status_code >= 400:
                raise decorators.GraphHTTPError(f"HTTP Error: {self.status_code}")

    def mock_get(*args, **kwargs):
        return MockResponse(kwargs.get('json_data', {}), kwargs.get('status_code', 200))

    def mock_post(*args, **kwargs):
        return MockResponse(kwargs.get('json_data', {}), kwargs.get('status_code', 200))

    def mock_patch(*args, **kwargs):
        return MockResponse(kwargs.get('json_data', {}), kwargs.get('status_code', 200))

    def mock_delete(*args, **kwargs):
        return MockResponse(kwargs.get('json_data', {}), kwargs.get('status_code', 200))

    monkeypatch.setattr(requests, 'get', mock_get)
    monkeypatch.setattr(requests, 'post', mock_post)
    monkeypatch.setattr(requests, 'patch', mock_patch)
    monkeypatch.setattr(requests, 'delete', mock_delete)
    
@patch('requests.get')
def test_get_group_by_name_success(mock_response):
    response_data = {
         'group_id': 'group_id', 'group_name': 'Test Group'
    }
    #mock_response(json_data=response_data, status_code=200)
    mock_response(monkeypatch=requests.get(json_data=response_data, status_code=200))

    result = get_group_by_name("Test Group", "fake_token")
    print(result)
    assert result == {'status_code': 200, 'group_id': 'group_id', 'group_name': 'Test Group'}

def test_get_group_by_name_no_match(mock_response):
    response_data = {
        '@odata.count': 0,
        'value': []
    }
    mock_response(response_data, status_code=200)
    result = get_group_by_name("No Group", "fake_token")
    assert result['error'] == 'No AAD group that contains No Group found. Try another name.'

@patch('requests.get')
def test_get_user_from_upn_success(mock_response):
    response_data = {
        'id': 'user_id',
        'userPrincipalName': 'user@domain.com',
        'jobTitle': 'Developer'
    }
    mock_response(json_data=response_data, status_code=200)
    result = get_user_from_upn("user@domain.com", "fake_token")
    assert result == {'status_code': 200, 'id': 'user_id', 'upn': 'user@domain.com', 'job_title': 'Developer'}

def test_get_user_membership_groups_success(mock_response):
    response_data = {
        'value': [{'displayName': 'Group1', 'id': 'group1_id'}, {'displayName': 'Group2', 'id': 'group2_id'}]
    }
    mock_response(json_data=response_data, status_code=200)
    result = get_user_membership_groups("user@domain.com", "fake_token")
    assert result['status_code'] == 200
    assert len(result['groups']) == 2

def test_if_user_member_of_success(mock_response):
    response_data = {
        'value': [{'displayName': 'Group1', 'id': 'group1_id'}, {'displayName': 'Group2', 'id': 'group2_id'}]
    }
    mock_response(json_data=response_data, status_code=200)
    result = if_user_member_of("user@domain.com", "Group1", "fake_token")
    assert result is True

def test_add_user_to_group_success(mock_response):
    mock_response(json_data={}, status_code=204)
    result = add_user_to_group("user@domain.com", "Test Group", "fake_token")
    assert result['status_code'] == 204
    assert 'User user@domain.com added to AAD group Test Group.' in result['message']

def test_remove_user_from_group_success(mock_response):
    mock_response(json_data={}, status_code=204)
    result = remove_user_from_group("user@domain.com", "Test Group", "fake_token")
    assert result['status_code'] == 204
    assert 'User user@domain.com removed from AAD group Test Group.' in result['message']

def test_user_reset_password_success(mock_response):
    mock_response(json_data={}, status_code=204)
    result = user_reset_password("user@domain.com", "fake_token", "new_password")
    assert result['status_code'] == 204
    assert 'User user@domain.com password was reset to new_password.' in result['message']

def test_user_revoke_sessions_success(mock_response):
    mock_response(json_data={}, status_code=204)
    result = user_revoke_sessions("user@domain.com", "fake_token")
    assert result['status_code'] == 204
    assert 'Sessions revoked for user user@domain.com.' in result['message']