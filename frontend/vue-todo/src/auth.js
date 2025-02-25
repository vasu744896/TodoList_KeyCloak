import Keycloak from "keycloak-js";

const keycloak = new Keycloak({
    url: "http://localhost:8180",  // Your Keycloak URL
    realm: "page",                 // Your realm
    clientId: "page-app"           // Your client ID
});

export const initKeycloak = (callback) => {
    keycloak.init({ onLoad: "login-required", checkLoginIframe: false })
        .then(authenticated => {
            if (!authenticated) {
                console.log("User not authenticated");
            }
            updateToken();
            callback();
        })
        .catch(error => console.error("Keycloak initialization failed", error));
};

// Function to refresh token automatically before it expires
const updateToken = () => {
    setInterval(() => {
        keycloak.updateToken(30) // Refresh 30 seconds before expiry
            .then(refreshed => {
                if (refreshed) {
                    console.log("Token refreshed:", keycloak.token);
                }
            })
            .catch(() => {
                console.warn("Token refresh failed. Logging out...");
                logout();
            });
    }, 10000); // Check every 10 seconds
};

export const getToken = () => keycloak.token || null;
export const logout = () => keycloak.logout();

export default keycloak;
