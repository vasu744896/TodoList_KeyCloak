<template>
    <nav>
        <h1>Vue To-Do App</h1>
        <button @click="logoutUser">Logout</button>
    </nav>
</template>

<script>
import { logout } from "../auth";

export default {
    methods: {
        logoutUser() {
            logout();
        }
    }
};
</script>

<style scoped>
nav {
    display: flex;
    justify-content: space-between;
    background: #333;
    color: white;
    padding: 10px;
}
button {
    background: red;
    color: white;
    border: none;
    padding: 5px 10px;
    cursor: pointer;
}
</style>
