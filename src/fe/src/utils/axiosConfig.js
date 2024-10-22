import axios from 'axios';

const backendURI = process.env.REACT_APP_CONNECT4_API_BASE_URI;
const protocol = process.env.REACT_APP_CONNECT4_API_PROTOCOL;
const baseURL = `${protocol}://${backendURI}`;

const axiosInstance = axios.create({
  baseURL: baseURL,
  withCredentials: true
});

export default axiosInstance;
export { backendURI };
