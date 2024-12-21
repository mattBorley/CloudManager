import {Box, Button, Card, FormControl, FormLabel, Heading, Input, VStack, Text, InputGroup, InputRightElement} from "@chakra-ui/react";
import '../styling/Login.css';
import {useNavigate} from "react-router-dom";
import {useState} from "react";

function Login() {
    const navigate = useNavigate()
    const handleLogin = () => {
        navigate("/main")
    };
    const toSignUp = () => {
        navigate("/signup")
    };
    const toPasswordRecovery = () => {
        navigate("/passwordrecovery")
    };
    const [showPassword, setShowPassword] = useState(false);

    const togglePasswordVisibility = () => {
        setShowPassword((prevShowPassword) => !prevShowPassword);
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
                            Login
                    </Heading>
                    <FormControl id={"email"} isRequired>
                        <FormLabel fontSize={"lg"}>
                            Email
                        </FormLabel>
                        <Input type={"email"} placeholder={"Enter your email"} width={"500px"} />
                    </FormControl>
                    <FormControl id={"password"} isRequired mb={6}>
                        <FormLabel fontSize={"lg"}>
                            Password
                        </FormLabel>
                        <InputGroup width={"500px"}>
                          <Input
                            type={showPassword ? "text" : "password"}
                            placeholder={"Enter your password"}
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
                    </FormControl>
                    <Button type={"submit"} bg={"#3e3e3e"} color={"white"} _hover={{ bg: "#4e4e4e"}} onClick={handleLogin}>
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