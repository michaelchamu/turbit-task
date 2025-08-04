//this exports a reusable instace of axios so that
//we d
import axios from "axios";
const API_ENDPOINT: string = import.meta.env.VITE_APP_API_ENDPOINT;

console.log(API_ENDPOINT)
const apiClient = axios.create({
    baseURL: API_ENDPOINT,
    headers: {
        'Content-Type': 'application/json',
        // You can add other headers like authorization token here
    },
});

// Define common API methods
const _get = (url: string, config = {}) => {
    return apiClient.get(url, config);
};

const _delete = (url: string, config = {}) => {
    return apiClient.delete(url, config);
};

const _put = (url: string, data = {}, config = {}) => {
    return apiClient.put(url, data, config);
};

const _post = (url: string, data = {}, config = {}) => {
    return apiClient.post(url, data, config);
};

// Export API methods
export { _get, _delete, _put, _post };