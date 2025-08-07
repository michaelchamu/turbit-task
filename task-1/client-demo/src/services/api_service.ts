import type { QueryParameters, UserReportInterface } from '../types/interfaces';
import { _get } from '../utils/http_utility';
//fetches user reports and returns a User

export const fetchReports = async (
    params?: QueryParameters
): Promise<UserReportInterface[]> => {
    try {
        const response = await _get(`/reports`, {
            params
        });
        if (response.status === 200)
            return response.data;
        return [];
    } catch (error) {
        throw error; // rethrow the error for further handling
    }
};