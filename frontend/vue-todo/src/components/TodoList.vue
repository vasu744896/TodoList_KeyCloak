<template>
    <div>
        <h1>To-Do List</h1>
        <input v-model="newTodo" placeholder="Add a new task" />
        <button @click="addNewTodo">Add</button>
        <ul>
            <li v-for="todo in todos" :key="todo.id">
                {{ todo.task }}
            </li>
        </ul>
    </div>
</template>

<script>
import { fetchTodos, addTodo } from "../api";

export default {
    data() {
        return {
            todos: [],
            newTodo: ""
        };
    },
    async created() {
        this.todos = await fetchTodos();
    },
    methods: {
        async addNewTodo() {
            if (!this.newTodo) return;
            const newTask = await addTodo(this.newTodo);
            if (newTask) {
                this.todos.push(newTask);
                this.newTodo = "";
            }
        }
    }
};
</script>

<style scoped>
input {
    padding: 5px;
    margin-right: 5px;
}
button {
    padding: 5px;
}
</style>