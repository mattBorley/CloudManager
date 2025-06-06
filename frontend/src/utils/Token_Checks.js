import axios from "axios";

export const getAccessToken = () => {
    const accessToken = localStorage.getItem('accessToken');
    console.log(`Access Token from getAccessToken: ${accessToken}`);
    return accessToken;
}

const decodeJWT = (token) => {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const decoded = JSON.parse(atob(base64));
    return decoded;
}

export const isTokenExpired = (token) => {
    try {
        const decoded = decodeJWT(token);
        return decoded.exp * 1000 < Date.now();
    } catch (error) {
        return true;
    }
}

export const refreshAccessToken = async () => {
    try {
        const refreshToken = localStorage.getItem('refreshToken')
        if (!isTokenExpired(refreshToken)) {
            const response = await axios.post('http://localhost:8000/api/tokens/refresh', {
                refreshToken: refreshToken,
            });

            const {accessToken} = response.data;
            localStorage.setItem('accessToken', accessToken);
            return accessToken
        }
        return null;
    } catch (error) {
        console.error('Error refreshing access token: ', error);
        return null;
    }
};