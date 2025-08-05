from unittest.mock import AsyncMock, patch
from bson import ObjectId
from fastapi.testclient import TestClient
import pytest
from ..main import app

client = TestClient(app)

@pytest.fixture
def mock_posts():
    return [
        {"_id": ObjectId(), "id": 1, "userId":"1", "title": "Post 1", "body":"Wow"},
        {"_id": ObjectId(), "id": 2, "userId":"2", "title": "Post 2", "body":"Noo"}
    ]

def test_fetch_posts_empty():
    """Test empty posts list response"""
    with patch('app.routes.posts.mongo_connector.mongodb') as mock_mongodb:
        # Mock the entire MongoDB chain
        mock_db = mock_mongodb.db
        mock_collection = mock_db['posts']
        
        # Setup method chain for the query
        mock_find = mock_collection.find.return_value
        mock_sort = mock_find.sort.return_value
        mock_limit = mock_sort.limit.return_value
        mock_limit.to_list = AsyncMock(return_value=[])
        
        response = client.get("/posts")
        assert response.status_code == 200
        
        # Verify the exact response structure
        assert response.json() == {
            "posts": [],
            "next_cursor": None, 
            "has_more": False,
            "count": 0
        }
        
        # Verify the MongoDB query was constructed correctly
        mock_collection.find.assert_called_once_with({})
        mock_find.sort.assert_called_once_with("_id", -1)
        mock_sort.limit.assert_called_once_with(21)  # limit + 1 for pagination check

def test_fetch_single_post(mock_posts: any):
    '''Fetches single comment with correct id'''
    with patch('app.routes.posts.mongo_connector.mongodb') as mock_mongodb:
         # Setup async mock chain
        mock_db = AsyncMock()
        mock_mongodb.db = mock_db
        
        mock_collection = AsyncMock()
        mock_db.__getitem__.return_value = mock_collection
        
        # Mock the async find_one operation
        mock_collection.find_one = AsyncMock(return_value=mock_posts[1])
        
        response = client.get("/posts/1")
        assert response.status_code == 200
        
        # Validate response structure
        assert response.json()["userId"] == 2
        assert response.json()["title"] == "Post 2"
        
        # Verify the database query
        mock_collection.find_one.assert_awaited_once_with({"id": 1})

def test_fetch_single_post_not_found():
    '''Returns 404 when comment doesn't exist'''
    with patch('app.routes.posts.mongo_connector.mongodb') as mock_mongodb:
        # Setup async mock chain
        mock_db = AsyncMock()
        mock_mongodb.db = mock_db
        
        mock_collection = AsyncMock()
        mock_db.__getitem__.return_value = mock_collection
        
        # Mock find_one returning None (post not found)
        mock_collection.find_one = AsyncMock(return_value=None)
        
        response = client.get("/posts/999")  # Non-existent ID
        assert response.status_code == 404
        assert response.json()["detail"] == "Post not found"
        
        # Verify the database query
        mock_collection.find_one.assert_awaited_once_with({"id": 999})

def test_fetch_list_of_posts(mock_posts: any):
    '''returns list of posts and 200 success'''
    with patch('app.routes.posts.mongo_connector.mongodb') as mock_mongodb:
        # Mock the entire MongoDB chain
        mock_db = mock_mongodb.db
        mock_collection = mock_db['posts']
        
        # Setup method chain for the query
        mock_find = mock_collection.find.return_value
        mock_sort = mock_find.sort.return_value
        mock_limit = mock_sort.limit.return_value
        mock_limit.to_list = AsyncMock(return_value=mock_posts)
        
        response = client.get("/posts")
        assert response.status_code == 200
        
        response_data = response.json()
        
        # Verify the structure and count
        assert isinstance(response_data, dict)
        assert "posts" in response_data
        assert len(response_data["posts"]) == 2
        assert response_data["count"] == 2
        assert response_data["has_more"] is False
        assert response_data["next_cursor"] is None
        
        # Verify first user's basic fields
        assert response_data["posts"][0]["id"] == 1
        assert response_data["posts"][0]["userId"] == 1
        assert response_data["posts"][0]["body"] == "Wow"
        assert response_data["posts"][0]["title"] == "Post 1"
        
        # Verify second user's basic fields
        assert response_data["posts"][1]["id"] == 2
        assert response_data["posts"][1]["userId"] == 2
        assert response_data["posts"][1]["body"] == "Noo"
        assert response_data["posts"][1]["title"] == "Post 2"
        # Verify the MongoDB query was constructed correctly
        mock_collection.find.assert_called_once_with({})
        mock_find.sort.assert_called_once_with("_id", -1)
        mock_sort.limit.assert_called_once_with(21)  # limit + 1 for pagination check