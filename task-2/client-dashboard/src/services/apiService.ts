import type { TimeSeriesDataPoint, QueryParameters } from '../types/interfaces';
import { _get } from '../utils/http_utility';


export const fetchTimeSeriesData = async (
    params?: QueryParameters
): Promise<TimeSeriesDataPoint[]> => {
    try {
        const response = await _get(`/aggregated_timeseries`, {
            params
        });
        if (response.status === 200 || response.status === 204) {
            return response.data;
        } else {
            throw new Error(`Unexpected response status: ${response.status}`);
        }

    } catch (error) {
        console.error('Error fetching time series data:', error);
        throw error; // rethrow the error for further handling
    }
};

export const fetchTurbineList = async ():
    Promise<string[]> => {
    try {
        const response = await _get(`/turbines`);
        //check if there are turbines in list or not
        if (response.status === 204) {
            console.info('No Turbines');
            return [];// just set the dropdown to empty for now
        }
        return response.data;
    } catch (error) {
        console.error('Error fetching Turbines List:', error);
        throw error;
    }
}