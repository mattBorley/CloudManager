import { Navigate } from "react-router-dom";
import { isLoggedIn } from "../utils/User_Checks";

export const ProtectedRouteFromLoggedOut = ({ children }) => {
    if (!isLoggedIn()) {
        return <Navigate to={"/login"} replace />;
    }
    return children;
};

export const ProtectedRouteFromLoggedIn = ({ children }) => {
    if (isLoggedIn()) {
        return <Navigate to={"/main"}/>;
    }
    return children;
}