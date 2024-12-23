import React from 'react';
import ReactDOM from 'react-dom/client';
import { ChakraProvider } from "@chakra-ui/react";
import './styling/index.css';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';

import SignUp from "./pages/SignUp";
import PasswordRecovery from "./pages/PasswordRecovery";
import Login from './pages/Login'
import Main from './pages/Main'
import PageTitle from "./components/PageTitle";
import Layout from "./components/Layout";

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <ChakraProvider>
      <Router>
          <Routes>
              {/*Navigate users to login page*/}
              <Route path="/" element={<Navigate to = "/login" replace/>}/>

              <Route path="/login" element={
                  <PageTitle title={"Login - Cloud Storage Manager"}>
                      <Login/>
                  </PageTitle>}
              />
              <Route path="/main" element={
                  <Layout>
                      <PageTitle title={"Main - Cloud Storage Manager"}>
                          <Main/>
                      </PageTitle>
                  </Layout>}
              />
              <Route path = "/signup" element={
                  <PageTitle title={"Sign Up - Cloud Storage Manager"}>
                      <SignUp/>
                  </PageTitle>}
              />
              <Route path = "/passwordrecovery" element={
                  <PageTitle title={"Recover your password - Cloud Storage Manager"}>
                      <PasswordRecovery/>
                  </PageTitle>}
              />
          </Routes>
      </Router>
    </ChakraProvider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();