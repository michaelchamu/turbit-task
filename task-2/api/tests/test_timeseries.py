from fastapi.testclient import TestClient
import pytest
from datetime import datetime
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi import HTTPException
from ..main import app

client = TestClient(app)

'''fetch all timeseries data with valid parameters'''

@pytest.mark.asyncio
async def test_fetch_timeseries_with_valid_parameters():
    """Test fetching timeseries data with valid parameters"""
    test_turbine_id = "TURBINE-001"
    test_start_date = datetime(2023, 1, 1)
    test_end_date = datetime(2023, 1, 2)
    
    mock_results = [
        {
            "_id": 5.0,
            "avg_wind_speed": 5.2,
            "average_power": 1500.5,
            "avg_azimuth": 120.3,
            "average_external_temperature": 15.2,
            "average_internal_temperature": 20.1,
            "average_rpm": 12.5,
            "count": 10
        },
        {
            "_id": 6.0,
            "avg_wind_speed": 6.1,
            "average_power": 1800.7,
            "avg_azimuth": 125.8,
            "average_external_temperature": 16.3,
            "average_internal_temperature": 21.2,
            "average_rpm": 13.2,
            "count": 15
        }
    ]

    with patch('api.routes.timeseries.mongo_connector.mongodb') as mock_mongodb:
        # Setup mock DB chain
        mock_db = MagicMock()
        mock_mongodb.db = mock_db
        
        # Mock collection and aggregation
        mock_collection = MagicMock()
        mock_db.__getitem__.return_value = mock_collection
        
        # Mock async iterator for aggregation
        mock_cursor = AsyncMock()
        mock_cursor.__aiter__.return_value = iter(mock_results)
        mock_collection.aggregate = AsyncMock(return_value=mock_cursor)
        
        # Make request with parameters
        response = client.get(
            "/aggregated_timeseries",
            params={
                "start_date": test_start_date.isoformat(),
                "end_date": test_end_date.isoformat(),
                "turbine_id": test_turbine_id
            }
        )
        
        # Verify response
        assert response.status_code == 200
        response_data = response.json()
        
        # Check response structure and values
        assert len(response_data) == 2
        assert response_data[0]["average_wind_speed"] == 5.2
        assert response_data[0]["average_power"] == 1500.5
        assert response_data[1]["average_wind_speed"] == 6.1
        assert response_data[1]["average_power"] == 1800.7
        
        # Verify aggregation pipeline was constructed correctly
        mock_collection.aggregate.assert_awaited_once()
        pipeline = mock_collection.aggregate.call_args[0][0]
        
        # Check match stage
        assert pipeline[0]["$match"] == {
            "timestamp": {"$gte": test_start_date, "$lt": test_end_date},
            "metadata.turbine_id": test_turbine_id
        }
        
        # Check bucket stage
        assert pipeline[1]["$bucket"]["groupBy"] == "$wind_speed"
        assert pipeline[1]["$bucket"]["boundaries"][0] == 0.0
        assert pipeline[1]["$bucket"]["boundaries"][-1] == 25.5  # max_wind + bin_size
        
        # Check other pipeline stages
        assert pipeline[2]["$match"] == {"_id": {"$ne": "out_of_range"}}
        assert pipeline[3]["$sort"] == {"_id": 1}

@pytest.mark.asyncio
async def test_fetch_timeseries_with_default_dates():
    """Test that default dates are used when none are provided"""
    with patch('api.routes.timeseries.mongo_connector.mongodb') as mock_mongodb:
        # Setup mock DB chain
        mock_db = MagicMock()
        mock_mongodb.db = mock_db
        
        mock_collection = MagicMock()
        mock_db.__getitem__.return_value = mock_collection
        
        mock_cursor = AsyncMock()
        mock_cursor.__aiter__.return_value = iter([])
        mock_collection.aggregate = AsyncMock(return_value=mock_cursor)
        
        # Make request without date parameters
        response = await client.get("/aggregated_timeseries")
        
        assert response.status_code == 200
        mock_collection.aggregate.assert_awaited_once()
        
        pipeline = mock_collection.aggregate.call_args[0][0]
        default_start = datetime.strptime('01.01.2016, 00:00', '%d.%m.%Y, %H:%M')
        default_end = datetime.strptime('02.01.2016, 00:00', '%d.%m.%Y, %H:%M')
        
        assert pipeline[0]["$match"]["timestamp"]["$gte"] == default_start
        assert pipeline[0]["$match"]["timestamp"]["$lt"] == default_end

@pytest.mark.asyncio
async def test_fetch_timeseries_invalid_dates():
    """Test that invalid date range returns 400 error"""
    with patch('api.routes.timeseries.mongo_connector.mongodb'):
        # Make request with start_date after end_date
        response = client.get(
            "/aggregated_timeseries",
            params={
                "start_date": "2023-01-02T00:00:00",
                "end_date": "2023-01-01T00:00:00"
            }
        )
        
        assert response.status_code == 400
        assert "start_date must be earlier than end_date" in response.json()["detail"]

'''fetch all data with invalid parameters'''
''''''