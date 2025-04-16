import React, { useRef, useState } from 'react';
import {
  Box,
  VStack,
  Button,
  Heading,
  Text,
  useDisclosure,
  AlertDialog,
  AlertDialogBody,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogContent,
  AlertDialogOverlay
} from '@chakra-ui/react';
import axios from "axios";

const CloudList = ({ cloudList }) => {
  const cloud_count = cloudList.length;

  const { isOpen, onOpen, onClose } = useDisclosure();
  const cancelRef = useRef();

  const [selectedCloud, setSelectedCloud] = useState(null);

  const confirmRemove = (cloudName) => {
    setSelectedCloud(cloudName);
    onOpen();
  };

  const handleLogout = async () => {
    if (!selectedCloud) return;
    try {
      console.log("Removing account: " + selectedCloud);
      const access_token = localStorage.getItem('accessToken');
      await axios.post(process.env.REACT_APP_BACKEND_URL + '/api/cloud/remove', {
        cloudName: selectedCloud,
        access_token
      }, {
        withCredentials: true,
      });
      onClose();
      window.location.reload();
    } catch (error) {
      console.error("Couldn't remove account: ", error.response);
      console.error('Status Code:', error.response.status);
      console.error('Response Data:', error.response.data);
    }
  };

  return (
    <Box
      name={"Clouds"}
      w={"100%"}
      maxH={"400px"}
      alignItems={"center"}
      overflowY={"auto"}
    >
      <VStack spacing={2} align={"center"} width={"100%"}>
        {cloud_count === 0 ? (
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
          cloudList.map((cloudName, index) => (
            <Box
              key={index}
              bg={"#4e4e4e"}
              width={"95.5%"}
              height={"50px"}
              display={"flex"}
              alignItems={"center"}
              justifyContent={"space-between"}
              borderColor={"#2e2e2e"}
              borderWidth={2}
              borderRadius={5}
              ml={2}
              mr={2}
              fontWeight={"semibold"}
              color={"white"}
              padding={2}
            >
              <Text fontWeight="semibold">{cloudName}</Text>
              <Button
                size="sm"
                colorScheme="red"
                variant="outline"
                onClick={() => confirmRemove(cloudName)}
              >
                Remove
              </Button>
            </Box>
          ))
        )}
      </VStack>

      <AlertDialog
        isOpen={isOpen}
        leastDestructiveRef={cancelRef}
        onClose={onClose}
        isCentered
      >
        <AlertDialogOverlay>
          <AlertDialogContent>
            <AlertDialogHeader fontSize="lg" fontWeight="bold">
              Remove Cloud Account
            </AlertDialogHeader>

            <AlertDialogBody>
              Are you sure you want to remove <b>{selectedCloud}</b>?
            </AlertDialogBody>

            <AlertDialogFooter>
              <Button ref={cancelRef} onClick={onClose}>
                Cancel
              </Button>
              <Button colorScheme="red" onClick={handleLogout} ml={3}>
                Remove
              </Button>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialogOverlay>
      </AlertDialog>
    </Box>
  );
};

export default CloudList;
