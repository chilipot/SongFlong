import { useRef } from 'react';
import axios from 'axios';

export const BASE_URL = 'http://192.168.99.100:5000';

export default axios.create({
    baseURL: BASE_URL,
    responseType: 'json'
});
