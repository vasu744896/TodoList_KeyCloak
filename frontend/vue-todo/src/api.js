import axios from "axios";
import { getToken } from "./auth";

const API_BASE_URL = "http://127.0.0.1:8000"; // Your FastAPI backend URL

// Fetch all To-Do items
export const fetchTodos = async () => {
    try {
        const token = getToken();
        if (!token) {
            console.error("❌ No token found. User might not be authenticated.");
            return [];
        }

        console.log("📡 Fetching todos with token:", token);

        const response = await axios.get(`${API_BASE_URL}/todos`, {
            headers: { Authorization: `Bearer ${token}` }
        });

        console.log("✅ Fetched todos:", response.data);
        return response.data;
    } catch (error) {
        console.error("❌ Error fetching todos:", error.response?.data || error.message);
        return [];
    }
};

// Add a new To-Do item
export const addTodo = async (title) => {
    try {
        const token = getToken();
        if (!token) {
            console.error("❌ No token found. Cannot add todo.");
            return null;
        }

        console.log("📝 Adding todo with token:", token, "Title:", title);

        const response = await axios.post(
            `${API_BASE_URL}/todos`,
            { title },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            }
        );

        console.log("✅ Added todo:", response.data);
        return response.data;
    } catch (error) {
        console.error("❌ Error adding todo:", error.response?.data || error.message);
        return null;
    }
};

// Update a To-Do item
export const updateTodo = async (id, completed) => {
    try {
        const token = getToken();
        if (!token) {
            console.error("❌ No token found. Cannot update todo.");
            return null;
        }

        console.log("🔄 Updating todo with token:", token, "ID:", id, "Completed:", completed);

        const response = await axios.put(
            `${API_BASE_URL}/todos/${id}`,
            { completed },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json"
                }
            }
        );

        console.log("✅ Updated todo:", response.data);
        return response.data;
    } catch (error) {
        console.error("❌ Error updating todo:", error.response?.data || error.message);
        return null;
    }
};

// Delete a To-Do item
export const deleteTodo = async (id) => {
    try {
        const token = getToken();
        if (!token) {
            console.error("❌ No token found. Cannot delete todo.");
            return null;
        }

        console.log("🗑️ Deleting todo with token:", token, "ID:", id);

        const response = await axios.delete(`${API_BASE_URL}/todos/${id}`, {
            headers: { Authorization: `Bearer ${token}` }
        });

        console.log("✅ Deleted todo:", response.data);
        return response.data;
    } catch (error) {
        console.error("❌ Error deleting todo:", error.response?.data || error.message);
        return null;
    }
};
