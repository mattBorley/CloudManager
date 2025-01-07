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
            confirmPassword
        };

        try {
            const response = await axios.post('http://localhost:8000/api/users/signup', newUser, {
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            // Log the status code and status text for debugging
            console.log("Response Status:", response.status);
            console.log("Response Status Text:", response.statusText);

            const data = response.data;

            if (response.status === 200 && data.success) {

                const { accessToken, refreshToken } = data;

                localStorage.setItem('accessToken', accessToken);
                localStorage.setItem('refreshToken', refreshToken);

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
            className={"Background-Box"}
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
                mt={10}>
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
                        <FormLabel fontSize={"lg"}>
                            Email
                        </FormLabel>
                        <Input type={"email"} placeholder={"Enter your email"} width={"500px"} onChange={handleEmailChange}/>
                    </FormControl>
                    <FormControl id={"userName"} isRequired>
                        <FormLabel fontSize={"lg"}>
                            Name
                        </FormLabel>
                        <Input type={"email"} placeholder={"Enter your name"} width={"500px"} onChange={handleNameChange}/>
                    </FormControl>
                    <FormControl id={"password"} isRequired mb={4}>
                        <FormLabel fontSize={"lg"}>
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
                              bg={"#3e3e3e"}
                              color={"white"}
                              _hover={{ bg: "#4e4e4e" }}
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
                        <FormLabel fontSize={"lg"}>
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
                              bg={"#3e3e3e"}
                              color={"white"}
                              _hover={{ bg: "#4e4e4e" }}
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
                    <Button type={"submit"} bg={"#3e3e3e"} color={"white"} _hover={{ bg: "#4e4e4e"}} onClick={handleSignUp} disabled={!validPassword || !passwordsMatch}>
                        Sign Up
                    </Button>
                    <Text mt="4" textAlign="center" fontSize="sm" color="#4a5568">
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