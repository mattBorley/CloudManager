import React, {useEffect, useState} from "react";
import {
    Box,
    Button,
    Card,
    FormControl,
    FormLabel,
    Heading,
    HStack,
    Input,
    Select,
    Text,
    VStack,
} from "@chakra-ui/react";
import {useNavigate} from "react-router-dom";
import axios from "axios";
import "../styling/addCloud.css";
import {useGoogleLogin} from "@react-oauth/google";

function AddCloud() {
    const navigate = useNavigate();
    const [cloudName, setCloudName] = useState(); // Get context methods and values
    const [selectedCloud, setSelectedCloud] = useState("");
    const [errorMessage, setErrorMessage] = useState("");

    const handleNameChange = (event) => {
        setCloudName(event.target.value);
    };

    async function dropbox_oauth_logic() {
        try {
            console.log(cloudName);
            const response = await axios.get("http://localhost:8000/api/dropbox/authorization", {
                withCredentials: true,
            });
            localStorage.setItem("cloudName", cloudName);
            window.location.href = response.data.auth_url
        } catch (error) {
            console.error("Error initiating Dropbox OAuth: ", error);
        }
    }

    const google_oauth_logic = useGoogleLogin(
        {
            flow: "auth-code",
            onSuccess: async (response) => {
                try {
                    console.log("OAuth response received:", response);

                    const accessToken = localStorage.getItem("accessToken");
                    if (!accessToken) {
                        console.error("No access token found in localStorage.");
                        throw new Error("Access token not found");
                    }
                    console.log("Access token found:", accessToken);

                    console.log("Sending request to backend with code:", response.code, "and cloud_name:", cloudName);

                    const apiResponse = await axios.get("http://localhost:8000/api/google/callback", {
                        params: { code: response.code, cloud_name: cloudName },
                        headers: { Authorization: `Bearer ${accessToken}` },
                        withCredentials: true,
                    });

                    console.log("API Response:", apiResponse.data);

                } catch (error) {
                    console.error("Error during Google login process:", error);
                    if (error.response) {
                        console.error("Error response from server:", error.response.data);
                    }
                }
            },
            onError: (error) => {
                console.error("Login failed:", error);
            },
            scope: "https://www.googleapis.com/auth/drive.metadata.readonly email profile",
            redirect_uri: process.env.GOOGLE_REDIRECT_URI
        }
    );

    const box_oauth_logic = async () => {
        console.log("Initiating Box OAuth.")
        try {
            const response = await axios.get("http://localhost:8000/api/box/authorization", {
                withCredentials: true,
            });
            console.log("Response: ", response)
            localStorage.setItem("cloudName", cloudName);
            window.location.href = response.data.auth_url; // Redirect user to Box OAuth URL
        } catch (error) {
            console.error("Error initiating Box OAuth:", error);
            setErrorMessage("Error initiating Box OAuth.");
        }
    }

    const toMain = () => {
        navigate("/main");
    };

    const addCloud = async () => {
        if (!selectedCloud) {
            setErrorMessage("No service selected.");
            return;
        }

        switch (selectedCloud) {
            case "google_drive":
                console.log("Google Drive selected. Proceeding with Google Drive setup...");
                setErrorMessage("");
                google_oauth_logic();
                break;
            case "box":
                console.log("Box selected. Proceeding with OneDrive setup...");
                setErrorMessage("");
                await box_oauth_logic()
                break;
            case "dropbox":
                console.log("Dropbox selected. Proceeding with Dropbox setup...");
                setErrorMessage("");
                await dropbox_oauth_logic();
                break;
            default:
                console.log("No service selected");
                setErrorMessage("No service selected.");
        }
    };

    useEffect(() => {}, [cloudName]); // React to cloudName change

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
                    <Heading as={"h1"} className={"Heading-style"} mb={6}>
                        Add Cloud Service
                    </Heading>
                    <FormControl id={"cloudService"} isRequired>
                        <FormControl fontSize={"18px"} color={"white"}>
                            Select Cloud <span style={{color: "#e74b4b"}}>*</span>
                        </FormControl>
                        <Select
                            placeholder="Select option"
                            bg="#4e4e4e"
                            color="white"
                            _hover={{bg: "#5e5e5e"}}
                            _focus={{bg: "#5e5e5e", borderColor: "gray.600"}}
                            variant="filled"
                            borderRadius="md"
                            value={selectedCloud}
                            onChange={(e) => setSelectedCloud(e.target.value)}
                        >
                            <option value="google_drive" style={{background: "#4e4e4e", color: "white"}} >
                                Google Drive
                            </option>
                            <option value="box" style={{background: "#4e4e4e", color: "white"}}>
                                Box
                            </option>
                            <option value="dropbox" style={{background: "#4e4e4e", color: "white"}}>
                                Dropbox
                            </option>

                        </Select>
                    </FormControl>
                    <FormControl id={"cloudName"} isRequired mb={6}>
                        <FormLabel fontSize={"18px"} color={"white"}>
                            Cloud Name
                        </FormLabel>
                        <Input
                            id="cloudNameInput"
                            placeholder={"Enter the chosen name of this storage cloud"}
                            width={"500px"}
                            onChange={handleNameChange}
                            color={"white"}
                        />
                    </FormControl>
                    {errorMessage && (
                        <Text color="red.500" mt={0}>
                            ❌ {errorMessage}
                        </Text>
                    )}
                    <HStack w={"100%"} h={"100%"} justifyContent={"space-between"} px={10}>
                        <Button
                            type={"button"}
                            bg={"#4e4e4e"}
                            color={"white"}
                            _hover={{bg: "#5e5e5e"}}
                            onClick={toMain}
                        >
                            Back
                        </Button>
                        <Button
                            type={"button"}
                            bg={"#4e4e4e"}
                            color={"white"}
                            _hover={{bg: "#5e5e5e"}}
                            onClick={addCloud}
                            disabled={!cloudName}
                        >
                            Add cloud
                        </Button>
                    </HStack>
                </VStack>
            </Box>
        </Card>
    );
}

export default AddCloud;
