import pytest
from unittest.mock import Mock, patch
import sys
import os
from exampleAPI import get_claude_response

@pytest.fixture
def mock_client():
    with patch('exampleAPI.client') as mock:
        mock_instance = Mock()
        mock_instance.messages.create.return_value = Mock(
            content=[Mock(text="Test response from Claude")]
        )
        mock.return_value = mock_instance
        yield mock

def test_get_claude_response_success(mock_client):
    with patch('exampleAPI.client', mock_client.return_value):
        response = get_claude_response("Hello Claude")
        assert isinstance(response, str)
        assert "Test response from Claude" in response

def test_get_claude_response_with_different_model(mock_client):
    with patch('exampleAPI.client', mock_client.return_value):
        response = get_claude_response(
            "Hello", 
            model_name="claude-3-opus-20240229"
        )
        assert isinstance(response, str)
        assert "Test response from Claude" in response

def test_get_claude_response_with_empty_message(mock_client):
    with patch('exampleAPI.client', mock_client.return_value):
        response = get_claude_response("")
        assert isinstance(response, str)
        assert "Test response from Claude" in response

def test_get_claude_response_error(mock_client):
    with patch('exampleAPI.client') as mock_client_patch:
        mock_client_patch.messages.create.side_effect = Exception("API Error")
        response = get_claude_response("Hello")
        assert "API 호출 중 오류 발생" in response
        assert "API Error" in response