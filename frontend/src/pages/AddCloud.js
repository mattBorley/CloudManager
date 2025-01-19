import {
    Button,
    Card,
    Heading,
    VStack,
    Box,
    FormControl,
    FormLabel,
    Input,
    InputGroup,
    HStack, Select
} from "@chakra-ui/react";
import React from "react";
import {useNavigate} from "react-router-dom";

function AddCloud() {
    const navigate = useNavigate()

    const toMain = () => {
        navigate("/main")
    }

    const addCloud = () => {
        navigate("/main")
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
                            Add Cloud Service
                    </Heading>
                    <FormControl id={"cloudService"} isRequired>
                        <FormControl fontSize={"18px"}>
                            Select Cloud <span style={{color: "#e74b4b"}}>*</span>
                        </FormControl>
                        <Select
                            placeholder={"Select option"}
                            bg={"#4e4e4e"}
                            color={"white"}
                            _hover={{ bg: "#5e5e5e" }}
                        >
                            <option value={"google_drive"}>Google Drive</option>
                            <option value={"onedrive"}>OneDrive</option>
                            <option value={"dropbox"}>Dropbox</option>
                            <option value={"AWS"}>AWS</option>
                        </Select>
                    </FormControl>
                    <FormControl id={"cloudName"} isRequired mb={6}>
                        <FormLabel fontSize={"18px"}>
                            Cloud Name
                        </FormLabel>
                        <Input placeholder={"Enter the chosen name of this storage cloud"} width={"500px"}/>
                    </FormControl>
                    <HStack
                        w={"100%"}
                        h={"100%"}
                        justifyContent={"space-between"}
                        px={10}
                    >
                        <Button type={"button"} bg={"#4e4e4e"} color={"white"} _hover={{ bg: "#5e5e5e"}} onClick={toMain}>
                            Back
                        </Button>
                        <Button type={"button"} bg={"#4e4e4e"} color={"white"} _hover={{ bg: "#5e5e5e"}} onClick={addCloud}>
                            Add cloud
                        </Button>
                    </HStack>
                </VStack>
            </Box>

        </Card>
    )
}

export default AddCloud;