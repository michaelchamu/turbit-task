from unittest.mock import AsyncMock, MagicMock, patch
from bson import ObjectId
from fastapi.testclient import TestClient
import pytest
from ..main import app

client = TestClient(app)

comments = [
            {"_id": ObjectId(), "id": 1, "postId":"1", "name": "Post 1", "email": "ddd@rrr.com", "body":"Wow"},
            {"_id": ObjectId(), "id": 2, "postId":"2", "name": "Post 2", "email": "dsss@rrr.com", "body":"Noo"},
             {"_id": ObjectId(), "id": 2, "postId":"2", "name": "Post 2", "email": "dsss@rrr.com", "body":"Noo"}
]

posts = [
        {"_id": ObjectId(), "id": 1, "userId":"1", "title": "Post 1", "body":"Wow"},
        {"_id": ObjectId(), "id": 2, "userId":"2", "title": "Post 2", "body":"Noo"}
]

@pytest.fixture
def mock_reports():
    return [
        {"_id": ObjectId(), "id": 1, "name":"Tom", "username": "tom34", "posts": posts, "comments": comments, "posts_count": 2, "comments_count": 3 },
        {"_id": ObjectId(), "id": 2, "name":"Adam", "username": "adam34", "posts": posts, "comments": comments, "posts_count": 2, "comments_count": 3}
    ]


def test_fetch_reports_empty():
    """Test empty reports list response"""
    with patch('app.routes.reports.mongo_connector.mongodb') as mock_mongodb:
        # Mock the entire MongoDB chain
        mock_db = mock_mongodb.db
        mock_collection = mock_db['users']
        
        # Setup method chain for aggregation (not find/sort/limit)
        mock_aggregate = mock_collection.aggregate.return_value
        mock_aggregate.to_list = AsyncMock(return_value=[])
        
        response = client.get("/reports")
        assert response.status_code == 200
        
        assert response.json() == []

        # Verify the MongoDB aggregation was called correctly
        mock_collection.aggregate.assert_called_once()
        
        # Verify the aggregation pipeline structure
        call_args = mock_collection.aggregate.call_args[0][0]
        # Check that pipeline contains expected stages
        pipeline_stages = [stage.keys() for stage in call_args]
        assert any('$skip' in stage for stage in pipeline_stages)
        assert any('$limit' in stage for stage in pipeline_stages)
        assert any('$lookup' in stage for stage in pipeline_stages)
        assert any('$addFields' in stage for stage in pipeline_stages)

def test_fetch_single_report(mock_reports: any):
    '''Fetches single comment with correct id'''
    with patch('app.routes.posts.mongo_connector.mongodb') as mock_mongodb:
        
# Setup base mock
        mock_db = AsyncMock()
        mock_mongodb.db = mock_db

        # Mock users collection
        mock_users = AsyncMock()
        mock_db.__getitem__.return_value = mock_users
        
        # Mock count_documents (user exists check)
        mock_users.count_documents = AsyncMock(return_value=1)
        
        # Mock the cursor returned by aggregate
        mock_cursor = MagicMock()
        mock_cursor.to_list = AsyncMock(return_value=[mock_reports[0]])
        mock_users.aggregate = MagicMock(return_value=mock_cursor)
        
        # Make request
        response = client.get("/reports/1")
        
        # Verify response
        assert response.status_code == 200
        response_data = response.json()
        
        # Check values
        assert response_data["id"] == 1
        assert response_data["name"] == "Tom"
        assert response_data["username"] == "tom34"
        assert len(response_data["posts"]) == 2
        assert len(response_data["comments"]) == 3
        assert response_data["posts_count"] == 2
        assert response_data["comments_count"] == 3
        
        # Verify database call structure
        mock_users.count_documents.assert_awaited_once_with({"id": 1}, limit=1)
        mock_users.aggregate.assert_called_once()

        pipeline = mock_users.aggregate.call_args[0][0]
        assert {"$match": {"id": 1}} in pipeline
        assert any(stage.get("$lookup", {}).get("from") == "posts" for stage in pipeline)
        assert any(stage.get("$lookup", {}).get("from") == "comments" for stage in pipeline)
        assert any("$addFields" in stage for stage in pipeline)

def test_fetch_single_report_not_found():
    '''Returns 404 when user doesn't exist'''
    with patch('app.routes.reports.mongo_connector.mongodb') as mock_mongodb:
        # Setup async mock chain
        mock_db = AsyncMock()
        mock_mongodb.db = mock_db
        
        # Mock users collection
        mock_users_collection = AsyncMock()
        mock_db.__getitem__.return_value = mock_users_collection
        
        # Mock count_documents returning 0 (user not found)
        mock_users_collection.count_documents = AsyncMock(return_value=0)
        
        response = client.get("/reports/999")  # Non-existent user ID
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"
        
        # Verify the database query
        mock_users_collection.count_documents.assert_awaited_once_with({"id": 999}, limit=1)

# def test_fetch_list_of_posts(mock_posts: any):
#     '''returns list of posts and 200 success'''
#     with patch('app.routes.posts.mongo_connector.mongodb') as mock_mongodb:
#         # Mock the entire MongoDB chain
#         mock_db = mock_mongodb.db
#         mock_collection = mock_db['posts']
        
#         # Setup method chain for the query
#         mock_find = mock_collection.find.return_value
#         mock_sort = mock_find.sort.return_value
#         mock_limit = mock_sort.limit.return_value
#         mock_limit.to_list = AsyncMock(return_value=mock_posts)
        
#         response = client.get("/posts")
#         assert response.status_code == 200
        
#         response_data = response.json()
        
#         # Verify the structure and count
#         assert isinstance(response_data, dict)
#         assert "posts" in response_data
#         assert len(response_data["posts"]) == 2
#         assert response_data["count"] == 2
#         assert response_data["has_more"] is False
#         assert response_data["next_cursor"] is None
        
#         # Verify first user's basic fields
#         assert response_data["posts"][0]["id"] == 1
#         assert response_data["posts"][0]["userId"] == 1
#         assert response_data["posts"][0]["body"] == "Wow"
#         assert response_data["posts"][0]["title"] == "Post 1"
        
#         # Verify second user's basic fields
#         assert response_data["posts"][1]["id"] == 2
#         assert response_data["posts"][1]["userId"] == 2
#         assert response_data["posts"][1]["body"] == "Noo"
#         assert response_data["posts"][1]["title"] == "Post 2"
#         # Verify the MongoDB query was constructed correctly
#         mock_collection.find.assert_called_once_with({})
#         mock_find.sort.assert_called_once_with("_id", -1)
#         mock_sort.limit.assert_called_once_with(21)  # limit + 1 for pagination check