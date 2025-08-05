from unittest.mock import AsyncMock, patch
from bson import ObjectId
from fastapi.testclient import TestClient
import pytest
from ..main import app

client = TestClient(app)

#turbines list
def mock_turbines():
    return [
        "Turbine 1", "Turbine 2", "Turbine 3"
    ]

def test_fetch_turbines_empty():
    '''test fetching empty turbines'''
    with patch('api.routes.timeseries.mongo_connector.mongodb') as mock_mongodb:
        # Setup mock data
        mock_turbines = ["Turbine 1", "Turbine 2", "Turbine 3"]
        
        # Mock the MongoDB chain
        mock_db = AsyncMock()
        mock_mongodb.db = mock_db
        
        mock_collection = AsyncMock()
        mock_db.__getitem__.return_value = mock_collection
        
        # Mock distinct() to return our test data
        mock_collection.distinct = AsyncMock(return_value=mock_turbines)
        
        # Make the request
        response = client.get("/turbines")
        
        # Verify response
        assert response.status_code == 200
        assert response.json() == mock_turbines
        
        # Verify database call
        mock_collection.distinct.assert_awaited_once_with('metadata.turbine_id')

'''fetch all turbine'''

'''fetch single turbines'''
