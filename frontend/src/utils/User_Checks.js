import {isTokenExpired} from "./Token_Checks";

export const isLoggedIn = () => {
    const accessToken = localStorage.getItem('accessToken');
    return accessToken && !isTokenExpired(accessToken);
}