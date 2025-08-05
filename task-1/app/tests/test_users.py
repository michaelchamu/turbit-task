from unittest.mock import AsyncMock, patch
from bson import ObjectId
from fastapi.testclient import TestClient
import pytest
from ..main import app

client = TestClient(app)

@pytest.fixture
def mock_users():
    return [
        {"_id": ObjectId(), "id": 1, "name": "User 1"},
        {"_id": ObjectId(), "id": 2, "name": "User 2"}
    ]

def test_read_users_empty():
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

