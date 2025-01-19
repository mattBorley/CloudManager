import {Box, Button, Card, FormControl, FormLabel, Heading, Input, VStack, Text, InputGroup, InputRightElement} from "@chakra-ui/react";
import '../styling/Login.css';
import {useNavigate} from "react-router-dom";
import React, {useState} from "react";
import axios from "axios";

function Login() {
    const navigate = useNavigate()

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    const isValidEmail = (email) => {
        return emailRegex.test(email);
    }


    const handleLogin = async (e) => {
        e.preventDefault();

        if (email === "" && password === "") {
            setErrorMessage("Please enter your credentials.");
        } else if (email === "" || !isValidEmail(email)){
            setErrorMessage("Please enter valid email.");
        } else if (password === "") {
            setErrorMessage("Please enter your password.");
        } else {

            const userLoggingIn = {
                email,
                password
            };

            try {
                const accessResponse = await axios.post('http://localhost:8000/api/users/login', userLoggingIn, {
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
                    console.log("Access Token: " + access_token)
                    localStorage.setItem('refreshToken', refresh_token);
                    console.log("Refresh Token: " + refresh_token)

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
                setErrorMessage('Error connecting to the server.');
            }
        }
    };

    const toSignUp = () => {
        navigate("/signup")
    };
    const toPasswordRecovery = () => {
        navigate("/passwordrecovery")
    };

    const togglePasswordVisibility = () => {
        setShowPassword((prevShowPassword) => !prevShowPassword);
    };

    const handleEmailChange = (event) => {
        setEmail(event.target.value);
    };

    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
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
                            Login
                    </Heading>
                    <FormControl id={"email"} isRequired>
                        <FormLabel fontSize={"18px"}>
                            Email
                        </FormLabel>
                        <Input type={"email"} placeholder={"Enter your email"} width={"500px"} onChange={handleEmailChange}/>
                    </FormControl>
                    <FormControl id={"password"} isRequired mb={6}>
                        <FormLabel fontSize={"18px"}>
                            Password
                        </FormLabel>
                        <InputGroup width={"500px"}>
                          <Input
                            type={showPassword ? "text" : "password"}
                            placeholder={"Enter your password"}
                            pr={20}
                            onChange={handlePasswordChange}
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
                        {errorMessage && (
                          <Text color="red.500" mt={2}>
                            ❌ {errorMessage}
                          </Text>
                        )}
                    </FormControl>
                    <Button type={"button"} bg={"#4e4e4e"} color={"white"} _hover={{ bg: "#5e5e5e"}} onClick={handleLogin}>
                        Log In
                    </Button>
                    <Text mt="4" textAlign="center" fontSize="sm" color="#4a5568">
                        Don't have an account?{" "}
                        <Button
                          variant="link"
                          color="#2b6cb0"
                          _hover={{ textDecoration: "underline" }}
                          onClick={toSignUp}
                        >
                            Sign Up
                        </Button>
                    </Text>
                    <Text mt="4" textAlign="center" fontSize="sm" color="#4a5568">
                        Forgotten Password?{" "}
                        <Button
                          variant="link"
                          color="#2b6cb0"
                          _hover={{ textDecoration: "underline" }}
                          onClick={toPasswordRecovery}
                        >
                            Recover Here
                        </Button>
                    </Text>
                </VStack>
            </Box>
        </Card>
    )
}

export default Login;