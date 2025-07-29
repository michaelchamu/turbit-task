import axios from 'axios';

const API_ENDPOINT = import.meta.env.API_ENDPOINT || 'http://localhost:8000';

export interface TimeSeriesDataPoint {
    timestamp: string;
    power: number;
    wind_speed: number;
    turbine_id: string;
    additional_data?: Record<string, any>;
}

interface QueryParameters {
    turbine_id?: string;
    start_date?: string;
    end_date?: string;
    limit?: number;
}


export const fetchTimeSeriesData = async (
    params?: QueryParameters
): Promise<TimeSeriesDataPoint[]> => {
    try {
        const response = await axios.get<TimeSeriesDataPoint[]>(`${API_ENDPOINT}/timeseries`, {
            params,
        });
        return response.data;
    } catch (error) {
        console.error('Error fetching time series data:', error);
        throw error; // rethrow the error for further handling
    }
};