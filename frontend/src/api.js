import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const askQuestion = async (text) => {
    try {
        const response = await axios.post(`${API_URL}/ask`, { text });
        return response.data;
    } catch (error) {
        console.error("API Error:", error);
        throw error;
    }
};
