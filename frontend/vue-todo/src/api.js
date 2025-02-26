import axios from "axios";
import { getToken } from "./auth";

const API_BASE_URL = "http://127.0.0.1:8000"; // FastAPI backend URL

// Fetch all To-Do items
export const fetchTodos = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/todos`, {
            headers: { Authorization: `Bearer ${getToken()}` }
        });

        // Map API response to match frontend expectations
        return response.data.map(todo => ({
            id: todo.id,
            task: todo.title, // Mapping 'title' to 'task'
            assigned_to: todo.user_id, // Mapping 'user_id' to 'assigned_to'
            completed: todo.completed
        }));

    } catch (error) {
        console.error("Error fetching todos:", error.response?.data || error.message);
        return [];
    }
};

// Add a new To-Do item (Only for Admins)
export const addTodo = async (task, assignedTo) => {
    try {
        const response = await axios.post(
            `${API_BASE_URL}/todos`,
            { title: task, user_id: assignedTo }, // Ensure correct JSON format
            {
                headers: {
                    Authorization: `Bearer ${getToken()}`,
                    "Content-Type": "application/json"
                }
            }
        );
        return response.data;
    } catch (error) {
        console.error("Error adding todo:", error.response?.data || error.message);
        return null;
    }
};

// Delete a To-Do item (Only for Admins)
export const deleteTodo = async (id) => {
    try {
        await axios.delete(`${API_BASE_URL}/todos/${id}`, {
            headers: { Authorization: `Bearer ${getToken()}` }
        });
        return true;
    } catch (error) {
        console.error("Error deleting todo:", error.response?.data || error.message);
        return false;
    }
};

// Update a To-Do item's completion status
export const updateTodoStatus = async (id, completed) => {
    try {
        const response = await axios.put(
            `${API_BASE_URL}/todos/${id}`,
            { completed }, // Updating completion status
            {
                headers: {
                    Authorization: `Bearer ${getToken()}`,
                    "Content-Type": "application/json"
                }
            }
        );
        return response.data;
    } catch (error) {
        console.error("Error updating todo:", error.response?.data || error.message);
        return null;
    }
};
