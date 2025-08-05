from unittest.mock import AsyncMock, patch
from bson import ObjectId
from fastapi.testclient import TestClient
import pytest
from ..main import app

client = TestClient(app)

@pytest.fixture
def mock_users():
    return [
        {"_id": ObjectId(), "id": 1, "username": "Tom", "email": "k@dor.op", "name":"Walter", "address": {
            "street": "123 Main St",
            "suite": "Apt 2",
            "city": "New York",
            "zipcode": "10001",
            "geo": {"lat": "40.7128", "lng": "-74.0060"}
        }, "phone":"2323234234", "website":"wwww.tr.com", "company": {
            "name": "Company 2",
            "catchPhrase": "Catchy phrase",
            "bs": "Business stuff"
        }},
        {"_id": ObjectId(), "id": 2, "username": "Pete", "email": "tom@er.ty",  "name":"Wendy", "address": {
            "street": "123 Main St",
            "suite": "Apt 2",
            "city": "New York",
            "zipcode": "10001",
            "geo": {"lat": "40.7128", "lng": "-74.0060"}
        }, "phone":"32232232", "website":"tes.io", "company": {
            "name": "Company 2",
            "catchPhrase": "Catchy phrase",
            "bs": "Business stuff"
        }}
    ]

def test_fetch_users_empty():
    """Test empty user list response"""
    with patch('app.routes.users.mongo_connector.mongodb') as mock_mongodb:
        # Mock the entire MongoDB chain
        mock_db = mock_mongodb.db
        mock_collection = mock_db['users']
        
        # Setup method chain for the query
        mock_find = mock_collection.find.return_value
        mock_sort = mock_find.sort.return_value
        mock_limit = mock_sort.limit.return_value
        mock_limit.to_list = AsyncMock(return_value=[])
        
        response = client.get("/users")
        assert response.status_code == 200
        
        # Verify the exact response structure
        assert response.json() == {
            "users": [],
            "next_cursor": None, 
            "has_more": False,
            "count": 0
        }
        
        # Verify the MongoDB query was constructed correctly
        mock_collection.find.assert_called_once_with({})
        mock_find.sort.assert_called_once_with("_id", -1)
        mock_sort.limit.assert_called_once_with(21)  # limit + 1 for pagination check

def test_fetch_single_user(mock_users: any):
    '''Fetches single user with correct id'''
    with patch('app.routes.users.mongo_connector.mongodb') as mock_mongodb:
         # Setup async mock chain
        mock_db = AsyncMock()
        mock_mongodb.db = mock_db
        
        mock_collection = AsyncMock()
        mock_db.__getitem__.return_value = mock_collection
        
        # Mock the async find_one operation
        mock_collection.find_one = AsyncMock(return_value=mock_users[1])
        
        response = client.get("/users/2")
        assert response.status_code == 200
        
        # Validate response structure
        assert response.json()["id"] == 2
        assert response.json()["name"] == "Wendy"
        
        # Verify the database query
        mock_collection.find_one.assert_awaited_once_with({"id": 2})

def test_fetch_single_user_not_found():
    '''Returns 404 when user doesn't exist'''
    with patch('app.routes.users.mongo_connector.mongodb') as mock_mongodb:
        # Setup async mock chain
        mock_db = AsyncMock()
        mock_mongodb.db = mock_db
        
        mock_collection = AsyncMock()
        mock_db.__getitem__.return_value = mock_collection
        
        # Mock find_one returning None (user not found)
        mock_collection.find_one = AsyncMock(return_value=None)
        
        response = client.get("/users/999")  # Non-existent ID
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"
        
        # Verify the database query
        mock_collection.find_one.assert_awaited_once_with({"id": 999})

def test_fetch_list_of_users(mock_users):
    '''returns list of users and 200 success'''
    with patch('app.routes.users.mongo_connector.mongodb') as mock_mongodb:
        # Mock the entire MongoDB chain
        mock_db = mock_mongodb.db
        mock_collection = mock_db['users']
        
        # Setup method chain for the query
        mock_find = mock_collection.find.return_value
        mock_sort = mock_find.sort.return_value
        mock_limit = mock_sort.limit.return_value
        mock_limit.to_list = AsyncMock(return_value=mock_users)
        
        response = client.get("/users")
        assert response.status_code == 200
        
        response_data = response.json()
        
        # Verify the structure and count
        assert isinstance(response_data, dict)
        assert "users" in response_data
        assert len(response_data["users"]) == 2
        assert response_data["count"] == 2
        assert response_data["has_more"] is False
        assert response_data["next_cursor"] is None
        
        # Verify first user's basic fields
        assert response_data["users"][0]["id"] == 1
        assert response_data["users"][0]["name"] == "Walter"
        assert response_data["users"][0]["username"] == "Tom"
        
        # Verify second user's basic fields
        assert response_data["users"][1]["id"] == 2
        assert response_data["users"][1]["name"] == "Wendy"
        assert response_data["users"][1]["username"] == "Pete"
        
        # Verify nested structures exist
        assert "address" in response_data["users"][0]
        assert "company" in response_data["users"][0]
        assert "geo" in response_data["users"][0]["address"]
        
        # Verify the MongoDB query was constructed correctly
        mock_collection.find.assert_called_once_with({})
        mock_find.sort.assert_called_once_with("_id", -1)
        mock_sort.limit.assert_called_once_with(21)  # limit + 1 for pagination check