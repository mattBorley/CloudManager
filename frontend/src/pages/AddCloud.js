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
        break;
      case "onedrive":
        console.log("OneDrive selected. Proceeding with OneDrive setup...");
        setErrorMessage("");
        break;
      case "dropbox":
        console.log("Dropbox selected. Proceeding with Dropbox setup...");
        setErrorMessage("");
        await dropbox_oauth_logic();
        break;
      case "AWS":
        console.log("AWS selected. Proceeding with AWS setup...");
        setErrorMessage("");
        break;
      default:
        console.log("No service selected");
        setErrorMessage("No service selected.");
    }
  };

  useEffect(() => {
    if (cloudName) {
      console.log("Cloud name updated:", cloudName); // This will print when cloudName changes
    }
  }, [cloudName]); // React to cloudName change

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
              Select Cloud <span style={{ color: "#e74b4b" }}>*</span>
            </FormControl>
            <Select
              placeholder={"Select option"}
              bg={"#4e4e4e"}
              color={"white"}
              _hover={{ bg: "#5e5e5e" }}
              value={selectedCloud}
              onChange={(e) => setSelectedCloud(e.target.value)}
            >
              <option value={"google_drive"} color={"#5e5e5e"}>
                Google Drive
              </option>
              <option value={"onedrive"}>OneDrive</option>
              <option value={"dropbox"}>Dropbox</option>
              <option value={"AWS"}>AWS</option>
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
              _hover={{ bg: "#5e5e5e" }}
              onClick={toMain}
            >
              Back
            </Button>
            <Button
              type={"button"}
              bg={"#4e4e4e"}
              color={"white"}
              _hover={{ bg: "#5e5e5e" }}
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
