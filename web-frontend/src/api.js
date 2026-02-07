import axios from 'axios';

const API_URL = 'http://localhost:8000/api/';

const api = axios.create({
    baseURL: API_URL,
});

export const setAuthToken = (username, password) => {
    const token = btoa(`${username}:${password}`);
    api.defaults.headers.common['Authorization'] = `Basic ${token}`;
};

export default api;
