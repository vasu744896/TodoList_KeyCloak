<template>
    <Navbar />
    <TodoList />
</template>

<script>
import Navbar from "../components/Navbar.vue";
import TodoList from "../components/TodoList.vue";

export default {
    components: {
        Navbar,
        TodoList
    }
};
</script>
