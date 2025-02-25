import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { initKeycloak } from "./auth";

initKeycloak(() => {
    createApp(App).use(router).mount("#app");
});
