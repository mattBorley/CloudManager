import React, {useState} from 'react';
import {Box, Button, Card, FormControl, FormLabel, Heading, Input, VStack, Text, HStack} from "@chakra-ui/react";
import '../styling/Login.css';
import {useNavigate} from "react-router-dom";

function PasswordRecovery() {
    const navigate = useNavigate()
    // const [email, setEmail] = useState('');
    //
    // const handleEmailChange = (event) => {
    //     const newEmail = event.target.value;
    //     const
    //
    // }
    const toLogin = () => {
        navigate("/login")
    }
    const recoverPassword = () => {
        var x = 3;
    }
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
                            Recover your password
                    </Heading>
                    <FormControl id={"email"} isRequired mb={"6"}>
                        <FormLabel fontSize={"lg"}>
                            Email
                        </FormLabel>
                        <Input type={"email"} placeholder={"Enter your email"} width={"500px"} />
                    </FormControl>
                    <HStack>
                        <Button type={"submit"} width={"100px"} mr={6} bg={"#3e3e3e"} color={"white"} _hover={{ bg: "#4e4e4e"}} onClick={toLogin}>
                            Back
                        </Button>
                        <Button type={"submit"} width={"100px"} bg={"#3e3e3e"} color={"white"} _hover={{ bg: "#4e4e4e"}} onClick={recoverPassword}>
                            Recover
                        </Button>
                    </HStack>
                </VStack>
            </Box>
        </Card>
    )
}

export default PasswordRecovery;