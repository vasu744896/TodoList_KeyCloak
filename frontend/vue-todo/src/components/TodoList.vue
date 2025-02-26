<template>
    <div>
        <h1>To-Do List</h1>
        
        <!-- Task Input Bar (Only for Admins) -->
        <div v-if="isAdmin">
            <input v-model="newTodo" placeholder="Assign a task" />
            <input v-model="assignedTo" placeholder="Assign to user" />
            <button @click="addNewTodo">Assign</button>
        </div>

        <ul>
            <li v-for="todo in todos" :key="todo.id">
                {{ todo.task }} <span v-if="isAdmin"> (Assigned to: {{ todo.assigned_to || 'N/A' }})</span>
            </li>
        </ul>
    </div>
</template>

<script>
import { fetchTodos, addTodo } from "../api";
import keycloak from "../auth";

export default {
    data() {
        return {
            todos: [],
            newTodo: "",
            assignedTo: "",
            userRole: []
        };
    },
    async created() {
        this.userRole = keycloak.tokenParsed?.realm_access?.roles || [];
        this.refreshTodos();
    },
    computed: {
        isAdmin() {
            return this.userRole.includes("admin");
        }
    },
    methods: {
        async refreshTodos() {
            this.todos = await fetchTodos();
            console.log("Fetched todos:", this.todos); // Debugging
        },
        async addNewTodo() {
            if (!this.newTodo || !this.assignedTo) return;
            await addTodo(this.newTodo, this.assignedTo);
            this.refreshTodos(); // Refresh list after adding task
            this.newTodo = "";
            this.assignedTo = "";
        }
    }
};
</script>
