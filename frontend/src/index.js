import React, {useEffect, useState} from 'react';
import ReactDOM from 'react-dom/client';
import { ChakraProvider } from "@chakra-ui/react";
import './styling/index.css';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';

import SignUp from "./pages/SignUp";
import PasswordRecovery from "./pages/PasswordRecovery";
import Login from './pages/Login'
import Main from './pages/Main'
import AddCloud from './pages/AddCloud'
import PageTitle from "./components/PageTitle";
import { ProtectedRouteFromLoggedOut, ProtectedRouteFromLoggedIn } from "./components/ProtectedRoutes";
import axios from "axios";

const CSRF_Token_Context = React.createContext(null);
const App = () => {
    const [csrfToken, setCsrfToken] = useState(null);

    return (
        <React.StrictMode>
            <CSRF_Token_Context.Provider value={csrfToken}>
                <ChakraProvider>
                    <Router>
                        <Routes>
                            {/*Navigate users to login page*/}
                            <Route path="/" element={<Navigate to = "/login" replace/>}/>
                            <Route path="/login" element={
                                <ProtectedRouteFromLoggedIn>
                                    <PageTitle title={"Login - Cloud Storage Manager"}>
                                        <Login setCsrfToken={setCsrfToken} />
                                    </PageTitle>
                                </ProtectedRouteFromLoggedIn>
                            }/>
                            <Route path = "/signup" element={
                                <ProtectedRouteFromLoggedIn>
                                    <PageTitle title={"Sign Up - Cloud Storage Manager"}>
                                        <SignUp setCsrfToken={setCsrfToken} />
                                    </PageTitle>
                                </ProtectedRouteFromLoggedIn>
                            }/>
                            <Route path = "/passwordrecovery" element={
                                <PageTitle title={"Recover your password - Cloud Storage Manager"}>
                                    <PasswordRecovery/>
                                </PageTitle>
                            }/>
                            <Route path="/main" element={
                                // <ProtectedRouteFromLoggedOut>
                                    <PageTitle title={"Main - Cloud Storage Manager"}>
                                        <Main/>
                                    </PageTitle>
                                // </ProtectedRouteFromLoggedOut>
                            }/>
                            <Route path="/addcloud" element={
                                // <ProtectedRouteFromLoggedOut>
                                   <PageTitle title={"Add Cloud Service - Cloud Storage Manager"}>
                                       <AddCloud/>
                                   </PageTitle>
                                // </ProtectedRouteFromLoggedOut>
                            }/>
                        </Routes>
                    </Router>
                </ChakraProvider>
            </CSRF_Token_Context.Provider>
        </React.StrictMode>
    )
}



const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <App/>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();

export { CSRF_Token_Context }