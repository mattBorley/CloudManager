import axios from "axios";
import { getAccessToken, isTokenExpired, refreshAccessToken} from "../utils/Token_Checks";


axios.interceptors.request.use(
    async (config) => {
        let accessToken = getAccessToken()
        console.log(`Access Token in Axios Intercept: ${accessToken}`);
        if (!accessToken) {
            console.log("Access token not found somehow.");
            return config;
        };

        const isExpired = isTokenExpired(accessToken)
        if (isExpired) {
            accessToken = await refreshAccessToken()
            if (!accessToken) {
                window.location.href = '/login';
                return config;
            }
        }

        config.headers['Authorization'] = `Bearer ${accessToken}`;
        return config;
    }, (error) => {
        return Promise.reject(error);
    }
)