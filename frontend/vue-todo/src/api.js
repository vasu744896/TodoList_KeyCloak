import axios from "axios";
import { getToken } from "./auth";

const API_BASE_URL = "http://127.0.0.1:8000"; // Your FastAPI backend URL

// Fetch all To-Do items
export const fetchTodos = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/todos`, {
            headers: { Authorization: `Bearer ${getToken()}` }
        });
        return response.data;
    } catch (error) {
        console.error("Error fetching todos:", error.response?.data || error.message);
        return [];
    }
};

// Add a new To-Do item
export const addTodo = async (task) => {  // Fix: changed 'title' to 'task'
    try {
        const response = await axios.post(
            `${API_BASE_URL}/todos`,
            { task },  // Fix: changed 'title' to 'task'
            { headers: { Authorization: `Bearer ${getToken()}`, "Content-Type": "application/json" } }
        );
        return response.data;
    } catch (error) {
        console.error("Error adding todo:", error.response?.data || error.message);
        return null;
    }
};
