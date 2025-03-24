import React, {useState} from 'react';
import { Box, Button, Card, FormControl, FormLabel, Heading, Input, VStack, Text, InputGroup, InputRightElement } from "@chakra-ui/react";
import '../styling/Login.css';
import {useNavigate} from "react-router-dom";
import axios from "axios";

function SignUp() {
    const navigate = useNavigate()
    const [email, setEmail] = useState('');
    const [name, setName] = useState('');
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [validPassword, setValidPassword] = useState(false);
    const [passwordsMatch, setPasswordsMatch] = useState(true);
    const [errorMessage, setErrorMessage] = useState("");


    const handleSignUp = async (e) => {

        e.preventDefault();

        const newUser = {
            email,
            name,
            password,
            confirm_password: confirmPassword
        };

        try {
            const accessResponse = await axios.post('http://localhost:8000/api/users/signup', newUser, {
                headers: {
                    'Content-Type': 'application/json',
                },
                withCredentials: true,
            });

            console.log("Response Status:", accessResponse.status);
            console.log("Response Status Text:", accessResponse.statusText);

            const data = accessResponse.data;

            console.log("Response Data: ", data)

            if (accessResponse.status === 200 && data.success) {

                const { access_token, refresh_token } = data;

                localStorage.setItem('accessToken', access_token);
                console.log("Access token: " + access_token)
                localStorage.setItem('refreshToken', refresh_token);
                console.log("Refresh token: " + refresh_token)

                const csrfResponse = await axios.get(
                    "api/tokens/get_csrf_token",
                    { withCredentials: true }
                );

                if (!(csrfResponse.data && csrfResponse.data.csrf_token)) {
                    setErrorMessage("CSRF Token not generated");
                    throw new Error("CSRF token not found in response");
                }

                navigate("/main");
            } else {
                setErrorMessage(typeof data.detail === 'string' ? data.detail : 'Error connecting to the server 2.');
            }
        } catch (error) {
            setErrorMessage('Error connecting to the server.')
        }
    }

    const toLogin = () => {
        navigate("/login")
    }

    const togglePasswordVisibility = () => {
        setShowPassword((prevShowPassword) => !prevShowPassword);
    };

    const passwordCriteria = [
    { id: 1, rule: "At least 8 characters", test: (password) => password.length >= 8 },
    { id: 2, rule: "At least one uppercase letter", test: (password) => /[A-Z]/.test(password) },
    { id: 3, rule: "At least one lowercase letter", test: (password) => /[a-z]/.test(password) },
    { id: 4, rule: "At least one number", test: (password) => /\d/.test(password) },
    { id: 5, rule: "At least one special character", test: (password) => /[!@#$%^&*(),.?":{}|<>]/.test(password) },
    ];

    const checkPasswordStrength = () => {
        return passwordCriteria.map(({ id, rule, test }) => (
          <Text key={id} color={test(password) ? "green.500" : "red.500"}>
            {test(password) ? "✔️" : "❌"} {rule}
          </Text>
        ));
    };

    const handleEmailChange = (event) => {
        setEmail(event.target.value);
    };

    const handleNameChange = (event) => {
        setName(event.target.value);
    };

    const handlePasswordChange = (event) => {
        const newPassword = event.target.value;
        setPassword(newPassword);

        const isValid = passwordCriteria.every(({ test }) => test(newPassword));
        setValidPassword(isValid);

        setPasswordsMatch(newPassword === confirmPassword);
    };

    const handleConfirmPasswordChange = (event) => {
        const newConfirmPassword = event.target.value;
        setConfirmPassword(newConfirmPassword);

        setPasswordsMatch(password === newConfirmPassword);
      };

    return(
        <Card
            bg={"#4e4e4e"}
            position={"absolute"}
            minH={"100%"}
            w={"100%"}
            p={4}
            display = "flex"
            alignItems={"center"}
            flexDir={"column"}
            borderRadius={"0"}
        >
            <Heading
                as={"h1"}
                className={"Heading-style"}
                mt={10}

            >
                Cloud Storage Manager
            </Heading>
            <Box
                bg={"#2e2e2e"}
                w={"600px"}
                p={12}
                display={"flex"}
                boxShadow={"lg"}
                borderRadius={"lg"}
                mt={20}
                justifyContent={"center"}
                flexDir="column"
            >
                <VStack>
                    <Heading
                        as={"h1"}
                        className={"Heading-style"}
                        mb={6}
                    >
                            Sign Up
                    </Heading>
                    <FormControl id={"email"} isRequired>
                        <FormLabel fontSize={"18px"} color={"white"}>
                            Email
                        </FormLabel>
                        <Input type={"email"} placeholder={"Enter your email"} width={"500px"} onChange={handleEmailChange}/>
                    </FormControl>
                    <FormControl id={"userName"} isRequired>
                        <FormLabel fontSize={"18px"} color={"white"}>
                            Name
                        </FormLabel>
                        <Input type={"email"} placeholder={"Enter your name"} width={"500px"} onChange={handleNameChange}/>
                    </FormControl>
                    <FormControl id={"password"} isRequired mb={4}>
                        <FormLabel fontSize={"18px"} color={"white"}>
                            Password
                        </FormLabel>
                        <InputGroup width={"500px"}>
                          <Input
                            type={showPassword ? "text" : "password"}
                            placeholder={"Enter your password"}
                            onChange={handlePasswordChange}
                            pr={20}
                          />
                          <InputRightElement width="4.5rem">
                            <Button
                              size="sm"
                              width={"40"}
                              onClick={togglePasswordVisibility}
                              bg={"#4e4e4e"}
                              color={"white"}
                              _hover={{ bg: "#5e5e5e" }}
                              borderRadius={2}
                              mr={2}
                            >
                              {showPassword ? "Hide" : "Show"}
                            </Button>
                          </InputRightElement>
                        </InputGroup>
                        <Box mt={3}>
                          {checkPasswordStrength()}
                        </Box>
                    </FormControl>
                    <FormControl id={"confirmPassword"} isRequired mb={6}>
                        <FormLabel fontSize={"18px"} color={"white"}>
                            Confirm Password
                        </FormLabel>
                        <InputGroup width={"500px"}>
                          <Input
                            type={showPassword ? "text" : "password"}
                            placeholder={"Re-enter your password"}
                            value={confirmPassword}
                            onChange={handleConfirmPasswordChange}
                            pr={20}
                          />
                          <InputRightElement width="4.5rem">
                            <Button
                              size="sm"
                              width={"40"}
                              onClick={togglePasswordVisibility}
                              bg={"#4e4e4e"}
                              color={"white"}
                              _hover={{ bg: "#5e5e5e" }}
                              borderRadius={2}
                              mr={2}
                            >
                              {showPassword ? "Hide" : "Show"}
                            </Button>
                          </InputRightElement>
                        </InputGroup>
                        {!passwordsMatch && confirmPassword && (
                          <Text color="red.500" mt={2}>
                            ❌ Passwords do not match.
                          </Text>
                        )}
                        {errorMessage && (
                          <Text color="red.500" mt={2}>
                            ❌ {errorMessage}
                          </Text>
                        )}
                    </FormControl>
                    <Button type={"submit"} bg={"#4e4e4e"} color={"white"} _hover={{ bg: "#5e5e5e"}} onClick={handleSignUp} disabled={!validPassword || !passwordsMatch}>
                        Sign Up
                    </Button>
                    <Text mt="4" textAlign="center" fontSize="sm" color="#7a8598">
                        Already have an account?{" "}
                        <Button
                          variant="link"
                          color="#2b6cb0"
                          _hover={{ textDecoration: "underline" }}
                          onClick={toLogin}
                        >
                            Log In
                        </Button>
                    </Text>
                </VStack>
            </Box>
        </Card>
    )
}

export default SignUp;