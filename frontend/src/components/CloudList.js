import React from 'react';
import {Box, VStack, Button, Heading} from '@chakra-ui/react';

const CloudList = ({cloudList}) => {
    const cloud_count = cloudList.length

    return (
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
                            justifyContent={"center"}
                            borderColor={"#2e2e2e"}
                            borderWidth={2}
                            borderRadius={5}
                            ml={2}
                            mr={2}
                            fontWeight={"semibold"}
                            color={"white"}
                        >
                            {cloudName}
                        </Box>
                    ))
                )}
            </VStack>
        </Box>
    );
};

export default CloudList;
