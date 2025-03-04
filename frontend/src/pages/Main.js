import '../styling/Main.css';
import '../styling/tabs.css';
import { Button, Heading, Card, Flex, VStack, Box, HStack } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";
import React, {useEffect, useState} from "react";

import TabsComponent from "../components/Tabs";
import CloudList from "../components/CloudList";
import axios from "axios";
import {getAccessToken} from "../utils/Token_Checks";

function Main() {
    const navigate = useNavigate();
    const [clouds, setClouds] = useState([]);

    const toLogin = () => {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        navigate("/login");
    }

    const toAddCloud = () => {
        navigate("/addcloud");
    }

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get("http://localhost:8000/api/data/get_data", {
                    withCredentials: true,
                    headers: {
                        'Authorization': `Bearer ${getAccessToken()}`,
                    }
                });
                setClouds(prevClouds => [...prevClouds, ...response.data]);
                console.log(response.data)
            } catch (error) {
                console.error("Error fetching cloud data:", error);
            }
        };

        fetchData();
    }, []);


    return (
        <Card
            name={"Background"}
            bg={"#4e4e4e"}
            minH={"100%"}
            w={"100%"}
            overflow={"auto"}
            p={4}
            display="flex"
            alignItems={"center"}
            borderRadius={"0"}
        >
            <HStack
                spacing={5}
                padding={5}
                alignItems="flex-start"
                w="max-content"
                mx="auto"
                mt={5}
                mb={10}
            >
                <Box
                    name={"SideBar"}
                    bg={"#2e2e2e"}
                    w={"400px"}
                    h={"800px"}
                    p={5}
                    display={"flex"}
                    boxShadow={"lg"}
                    borderRadius={"lg"}
                    alignItems={"center"}
                    flexDir="column"
                >
                    <Flex
                        direction={"column"}
                        justifyContent={"space-between"}
                        h={"100%"}
                        w={"100%"}
                    >
                        <Heading
                            name={"Title: Cloud Storage Manager"}
                            as={"h1"}
                            className={"Heading-style"}
                            mb={20}
                        >
                            Cloud Storage Manager
                        </Heading>
                        <Flex
                            flexDirection={"column"}
                            justifyContent={"space-between"}
                            height={"90%"}
                            width={"100%"}
                        >
                            <Box
                                name={"Cloud Services Box"}
                                bg={"#4e4e4e"}
                                w={"360px"}
                                maxH={"500px"}
                                display={"flex"}
                                boxShadow={"lg"}
                                borderRadius={"lg"}
                                justifyContent={"flex-start"}
                                flexDir={"column"}
                                pb={3}
                            >
                                <VStack
                                    spacing={2}
                                    align={"stretch"}
                                >
                                    <Flex
                                        mt={2}
                                        mb={2}
                                        alignItems="center"
                                        justifyContent="space-between"
                                        width={"100%"}
                                    >
                                        <Box
                                            ml={4}
                                            justifyContent={"center"}
                                            mb={1}
                                        >
                                            <Heading as="h2" size="md" color={"white"}>
                                                Cloud Services
                                            </Heading>
                                        </Box>
                                        <Box
                                            mr={2}
                                        >
                                            <Button
                                                bg="#2e2e2e"
                                                size="sm"
                                                borderRadius="md"
                                                _hover={{bg: "#1e1e1e"}}
                                                onClick={toAddCloud}
                                                color={"white"}
                                            >
                                                Add Cloud
                                            </Button>
                                        </Box>
                                    </Flex>
                                    <CloudList cloudList={clouds.map(cloud => cloud.cloud_name) || []}/>
                                </VStack>
                            </Box>
                            <Box ml={"auto"}>
                                <Button
                                    bg="#4e4e4e"
                                    size="sm"
                                    borderRadius="md"
                                    _hover={{bg: "#5e5e5e"}}
                                    onClick={toLogin}
                                    color={"white"}
                                >
                                    Log Out
                                </Button>
                            </Box>
                        </Flex>
                    </Flex>
                </Box>
                <Box
                    bg={"#2e2e2e"}
                    w={"1200px"}
                    h={"800px"}
                    p={2}
                    display={"flex"}
                    boxShadow={"lg"}
                    borderRadius={"lg"}
                    alignItems={"center"}
                    flexDir="column"
                >
                    <TabsComponent cloudData={clouds}/>
                </Box>
            </HStack>
        </Card>
    );
}

export default Main;
