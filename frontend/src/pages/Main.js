import '../styling/Main.css';
import '../styling/tabs.css';
import {Button, Heading, Card, Flex, VStack, Box, HStack} from "@chakra-ui/react";
import {useNavigate} from "react-router-dom";
import React, {useState} from "react";

import TabsComponent from "../components/Tabs";

function Main() {
    const navigate = useNavigate()

    const [cloudCount, setCloudCount] = useState(0);
    const cloudNames = ["GoogleDrive", "Cloud 2", "DropBox", "Cloud 4"];

    const toLogin = () => {
        // localStorage.removeItem('accessToken')
        // localStorage.removeItem('refreshToken')
        //
        // navigate("/login")
        if (cloudCount === 0) setCloudCount(11);
        if (cloudCount === 11) setCloudCount(0);
    }

    const toAddCloud = () => {
        navigate("/addcloud")
    }

    const handleAddButton = () => {
        setCloudCount(cloudCount + 1);
    }

    const handleRemoveButton = () => {
        if (cloudCount > 0) setCloudCount(cloudCount - 1);
    }

    return (
        <Card
            name={"Background"}
            bg={"#4e4e4e"}
            minH={"100%"}
            w={"100%"}
            overflow={"auto"}
            p={4}
            display = "flex"
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
                                            <Heading as="h2" size="md">
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
                                                _hover={{ bg: "#1e1e1e" }}
                                                onClick={toAddCloud}
                                            >
                                                Add Cloud
                                            </Button>
                                        </Box>
                                    </Flex>
                                    <Box
                                        name={"Clouds"}
                                        w={"100%"}
                                        maxH={"400px"}
                                        alignItems={"center"}
                                        overflowY={"auto"}
                                    >
                                        <VStack
                                            spacing={2}
                                            align={"center"}
                                            width={"100%"}
                                        >
                                            {cloudCount === 0 ? (
                                                <Box
                                                    bg={"#4e4e4e"}
                                                    width={"95.5%"}
                                                    height={"50px"}
                                                    display={"flex"}
                                                    alignItems={"center"}
                                                    justifyContent={"center"}
                                                    borderColor={"#2e2e2e"}
                                                    borderWidth={2}
                                                    borderRadius={5}
                                                    ml={2}
                                                    mr={2}
                                                >
                                                    <Heading as="h4" size="sm" color="#fff" fontWeight={"semibold"}>
                                                        No Clouds Connected
                                                    </Heading>
                                                </Box>
                                            ) : (
                                                Array.from({ length: cloudCount }).map((_, index) =>(
                                                    <Button

                                                        key={index}
                                                        bg={"#2e2e2e"}
                                                        width={"95.5%"}
                                                        height={"50px"}
                                                        shadow={"lg"}
                                                        ml={2}
                                                        mr={2}
                                                        fontWeight={"semibold"}
                                                        as={"h4"}

                                                    >
                                                        {cloudNames[index]}
                                                    </Button>
                                                ))
                                            )}
                                        </VStack>
                                    </Box>
                                </VStack>
                            </Box>
                            <Box
                                ml={"auto"}
                            >
                                <Button
                                    bg="#4e4e4e"
                                    size="sm"
                                    borderRadius="md"
                                    _hover={{ bg: "#5e5e5e" }}
                                    onClick={toLogin}
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
                    <TabsComponent/>
                </Box>
            </HStack>
        </Card>
    );
}

export default Main;