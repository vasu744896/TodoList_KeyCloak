import Keycloak from "keycloak-js";

const keycloak = new Keycloak({
    url: "http://localhost:8180",
    realm: "page",
    clientId: "page-app",
    credentials: { secret: "your-client-secret" } // Replace with your actual secret
});

// Initialize Keycloak and handle authentication
export const initKeycloak = (callback) => {
    keycloak.init({
        onLoad: "login-required",
        checkLoginIframe: false,
    })
    .then(authenticated => {
        if (!authenticated) {
            console.error("❌ User not authenticated!");
            return;
        }
        console.log("✅ User authenticated!", keycloak.token);
        updateToken();
        callback();
    })
    .catch(error => console.error("❌ Keycloak initialization failed", error));
};

// Function to refresh token automatically before it expires
const updateToken = () => {
    setInterval(() => {
        keycloak.updateToken(60)
            .then(refreshed => {
                if (refreshed) {
                    console.log("🔄 Token refreshed!");
                } else {
                    console.log("ℹ️ Token is still valid.");
                }
            })
            .catch(() => {
                console.warn("❌ Token refresh failed. Logging out...");
                logout();
            });
    }, 60000);
};

// Function to retrieve token
export const getToken = () => {
    if (!keycloak.token) {
        console.error("❌ No token available!");
        return null;
    }
    console.log("🔑 Retrieved Token:", keycloak.token);
    return keycloak.token;
};

// Function to logout user
export const logout = () => {
    console.log("🚪 Logging out...");
    keycloak.logout();
};

export default keycloak;
