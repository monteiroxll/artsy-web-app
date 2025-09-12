"""
Unit tests for the Artsy Web Service Flask application.
Tests cover all API endpoints, error handling, and core functionality.
"""

import pytest
import json
from unittest.mock import patch, Mock
from flask import Flask
import requests

# Import the main application
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app, fetch_token


class TestArtsyWebService:
    """Test suite for the Artsy Web Service application."""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the Flask application."""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    @pytest.fixture
    def mock_artsy_response(self):
        """Mock Artsy API response data."""
        return {
            "_embedded": {
                "artists": [
                    {
                        "id": "4d8b92b34eb68a1b2c0003f4",
                        "name": "Pablo Picasso",
                        "slug": "pablo-picasso",
                        "birthday": "1881",
                        "deathday": "1973",
                        "nationality": "Spanish"
                    },
                    {
                        "id": "4d8b92b34eb68a1b2c0003f5",
                        "name": "Vincent van Gogh",
                        "slug": "vincent-van-gogh",
                        "birthday": "1853",
                        "deathday": "1890",
                        "nationality": "Dutch"
                    }
                ]
            }
        }
    
    @pytest.fixture
    def mock_artist_detail(self):
        """Mock detailed artist information."""
        return {
            "id": "4d8b92b34eb68a1b2c0003f4",
            "name": "Pablo Picasso",
            "slug": "pablo-picasso",
            "birthday": "1881",
            "deathday": "1973",
            "nationality": "Spanish",
            "biography": "Pablo Ruiz Picasso was a Spanish painter, sculptor, printmaker, ceramicist and theatre designer who spent most of his adult life in France.",
            "published_artworks_count": 1234,
            "exhibition_highlights": []
        }

    def test_root_endpoint(self, client):
        """Test the root endpoint returns the main page."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Artist Search' in response.data
        assert b'search-form' in response.data

    def test_search_artist_success(self, client, mock_artsy_response):
        """Test successful artist search."""
        with patch('main.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = mock_artsy_response
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            response = client.get('/api/search?q=picasso')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert '_embedded' in data
            assert 'artists' in data['_embedded']
            assert len(data['_embedded']['artists']) == 2

    def test_search_artist_no_query(self, client):
        """Test search endpoint with no query parameter."""
        response = client.get('/api/search')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'No query provided'

    def test_search_artist_empty_query(self, client):
        """Test search endpoint with empty query."""
        response = client.get('/api/search?q=')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'No query provided'

    def test_search_artist_api_error(self, client):
        """Test search endpoint when Artsy API returns an error."""
        with patch('main.requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.RequestException("API Error")
            
            response = client.get('/api/search?q=picasso')
            
            assert response.status_code == 500
            data = json.loads(response.data)
            assert 'error' in data
            assert 'API Error' in data['error']

    def test_get_artist_success(self, client, mock_artist_detail):
        """Test successful artist detail retrieval."""
        with patch('main.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = mock_artist_detail
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            response = client.get('/api/artist/4d8b92b34eb68a1b2c0003f4')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['id'] == '4d8b92b34eb68a1b2c0003f4'
            assert data['name'] == 'Pablo Picasso'
            assert data['nationality'] == 'Spanish'

    def test_get_artist_no_id(self, client):
        """Test get artist endpoint with no artist ID."""
        response = client.get('/api/artist/')
        assert response.status_code == 404  # Flask returns 404 for missing path parameter

    def test_get_artist_empty_id(self, client):
        """Test get artist endpoint with empty artist ID."""
        response = client.get('/api/artist/')
        assert response.status_code == 404

    def test_get_artist_api_error(self, client):
        """Test get artist endpoint when Artsy API returns an error."""
        with patch('main.requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.RequestException("Artist not found")
            
            response = client.get('/api/artist/4d8b92b34eb68a1b2c0003f4')
            
            assert response.status_code == 500
            data = json.loads(response.data)
            assert 'error' in data
            assert 'Artist not found' in data['error']

    def test_fetch_token_success(self):
        """Test successful token fetching."""
        with patch('main.requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"token": "test_token_123"}
            mock_post.return_value = mock_response
            
            # Call fetch_token function
            fetch_token()
            
            # Verify the token was set (we can't directly test the global variable,
            # but we can verify the request was made correctly)
            mock_post.assert_called_once()
            call_args = mock_post.call_args
            assert 'artsy.net/api/tokens/xapp_token' in call_args[0][0]

    def test_fetch_token_failure(self):
        """Test token fetching when API returns error."""
        with patch('main.requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 401
            mock_post.return_value = mock_response
            
            # Call fetch_token function
            fetch_token()
            
            # Verify the request was made
            mock_post.assert_called_once()

    def test_search_artist_with_headers(self, client, mock_artsy_response):
        """Test that search request includes proper headers."""
        with patch('main.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = mock_artsy_response
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            client.get('/api/search?q=picasso')
            
            # Verify headers were set correctly
            call_args = mock_get.call_args
            headers = call_args[1]['headers']
            assert 'X-XAPP-Token' in headers
            assert headers['Content-Type'] == 'application/json'

    def test_get_artist_with_headers(self, client, mock_artist_detail):
        """Test that get artist request includes proper headers."""
        with patch('main.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = mock_artist_detail
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            client.get('/api/artist/4d8b92b34eb68a1b2c0003f4')
            
            # Verify headers were set correctly
            call_args = mock_get.call_args
            headers = call_args[1]['headers']
            assert 'X-XAPP-Token' in headers
            assert headers['Content-Type'] == 'application/json'

    def test_static_files_served(self, client):
        """Test that static files are properly served."""
        # Test CSS file
        response = client.get('/static/style.css')
        assert response.status_code == 200
        assert response.content_type == 'text/css; charset=utf-8'
        
        # Test JavaScript file
        response = client.get('/static/script.js')
        assert response.status_code == 200
        assert 'application/javascript' in response.content_type

    def test_template_rendering(self, client):
        """Test that the main template renders correctly."""
        response = client.get('/')
        assert response.status_code == 200
        
        # Check for key elements in the template
        assert b'search-input' in response.data
        assert b'search-button' in response.data
        assert b'clear-input' in response.data
        assert b'result-list' in response.data
        assert b'artsy_logo.svg' in response.data

    def test_error_handling_json_response(self, client):
        """Test that error responses are in JSON format."""
        # Test 400 error
        response = client.get('/api/search')
        assert response.status_code == 400
        assert response.content_type == 'application/json'
        
        # Test 500 error
        with patch('main.requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.RequestException("Test error")
            response = client.get('/api/search?q=test')
            assert response.status_code == 500
            assert response.content_type == 'application/json'


class TestIntegration:
    """Integration tests for the complete application flow."""
    
    @pytest.fixture
    def client(self):
        """Create a test client for integration testing."""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_complete_search_flow(self, client):
        """Test the complete search flow from frontend to API."""
        # Test that the main page loads
        response = client.get('/')
        assert response.status_code == 200
        
        # Test that static assets are accessible
        css_response = client.get('/static/style.css')
        assert css_response.status_code == 200
        
        js_response = client.get('/static/script.js')
        assert js_response.status_code == 200

    def test_api_endpoints_accessible(self, client):
        """Test that all API endpoints are accessible."""
        # Test search endpoint (should return 400 for missing query)
        response = client.get('/api/search')
        assert response.status_code == 400
        
        # Test artist endpoint (should return 500 for invalid ID due to API call)
        with patch('main.requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.RequestException("Test")
            response = client.get('/api/artist/test-id')
            assert response.status_code == 500


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

