import axios from 'axios';

const API_ENDPOINT = import.meta.env.API_ENDPOINT || 'http://localhost:8000';

export interface TimeSeriesDataPoint {
    average_wind_speed: number;
    average_power: number;
}

interface QueryParameters {
    turbine_id?: string;
    start_date?: string;
    end_date?: string;
}


export const fetchTimeSeriesData = async (
    params?: QueryParameters
): Promise<TimeSeriesDataPoint[]> => {
    try {
        const response = await axios.get<TimeSeriesDataPoint[]>(`${API_ENDPOINT}/aggregated_timeseries`, {
            params
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching time series data:', error);
        throw error; // rethrow the error for further handling
    }
};