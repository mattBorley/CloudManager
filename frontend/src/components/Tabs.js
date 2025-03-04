import { Box, Flex, Tab, TabList, TabPanel, TabPanels, Tabs, Text } from "@chakra-ui/react";
import React from "react";
import TreeMap from "./Graphs/TreeMap";
import PieChart from "./Graphs/PieChart";
import { GraphDataProvider } from "./Graphs/GetData"; // ✅ Fixed Import Path

// ✅ Function to format storage size in GB or MB
const formatStorageSize = (bytes) => {
    if (bytes >= 1e9) {
        return `${(bytes / 1e9).toFixed(2)} GB`;
    } else if (bytes >= 1e6) {
        return `${(bytes / 1e6).toFixed(2)} MB`;
    } else {
        return `${bytes} bytes`;
    }
};

const TabsComponent = ({ cloudData }) => {
    return (
        <Tabs variant="enclosed" bg="#4e4e4e" borderRadius={5} width="100%" height="100%" isFitted>
            <TabList borderColor="#ffffff" h="8%">
                {cloudData.length > 0 ? (
                    cloudData.map((cloud, index) => (
                        <Tab
                            key={index}
                            as="h1"
                            fontWeight="semibold"
                            borderRadius={2}
                            borderWidth={3}
                            _selected={{ color: "#2b6cb0", borderColor: "#2b6cb0" }}
                            color="white"
                            _hover={{ color: "#95b0d8", borderColor: "#95b0d8" }}
                        >
                            {cloud.cloud_name}
                        </Tab>
                    ))
                ) : (
                    <Tab isDisabled _disabled={{ cursor: "default" }} borderColor="#ffffff">
                        No Tabs Available
                    </Tab>
                )}
            </TabList>

            <TabPanels borderColor="#2e2e2e" h="92%">
                {cloudData.length > 0 ? (
                    cloudData.map((cloud, index) => (
                        <TabPanel key={index} shadow="bg" h="100%" p={2}>
                            <Flex w="100%" h="100%" justifyContent="space-between" alignItems="center">
                                <Box bg="#4e4e4e" w="30%" h="98%" p={4} borderRadius={5} overflowY="auto">
                                    <p className="title">Storage Information:</p>
                                    <div className="row">
                                        <p className="label">Storage used:</p>
                                        <p className="value">{formatStorageSize(cloud.cloud_data.storage.used_storage)}</p>
                                    </div>
                                    <div className="row">
                                        <p className="label">Capacity:</p>
                                        <p className="value">{formatStorageSize(cloud.cloud_data.storage.total_storage)}</p>
                                    </div>
                                    <div className="row">
                                        <p className="label">Remaining Storage:</p>
                                        <p className="value">{formatStorageSize(cloud.cloud_data.storage.remaining_storage)}</p>
                                    </div>
                                    <div className="row">
                                        <p className="label">Number of files:</p>
                                        <p className="value">{cloud.cloud_data.file_metadata.file_count}</p>
                                    </div>
                                    <div className="row">
                                        <p className="label">Largest File:</p>
                                        <p className="value">
                                            {cloud.cloud_data.file_metadata.largest_file.name} (
                                            {formatStorageSize(cloud.cloud_data.file_metadata.largest_file.size)})
                                        </p>
                                    </div>
                                    <div className="row">
                                        <p className="label">Oldest File:</p>
                                        <p className="value">
                                            {cloud.cloud_data.file_metadata.oldest_file.name} - Last Modified:{" "}
                                            {cloud.cloud_data.file_metadata.oldest_file.modified}
                                        </p>
                                    </div>
                                    <div className="row">
                                        <p className="label">Number of duplicates:</p>
                                        <p className="value">{cloud.cloud_data.duplicates.duplicate_count}</p>
                                    </div>
                                    <div className="row">
                                        <p className="label">Storage used by duplicates:</p>
                                        <p className="value">{formatStorageSize(cloud.cloud_data.duplicates.storage_used_by_duplicates)}</p>
                                    </div>
                                    <div className="row">
                                        <p className="label">Last Synced:</p>
                                        <p className="value">{cloud.cloud_data.sync_info.last_synced}</p>
                                    </div>
                                </Box>
                                <GraphDataProvider cloudData={cloud.cloud_data.storage}>
                                    <Box
                                        bg="#2e2e2e"
                                        w="68%"
                                        h="98%"
                                        p={4}
                                        borderRadius={5}
                                        shadow="md"
                                        display="flex"
                                        flexDir="column"
                                        justifyContent="center"
                                        alignItems="center"
                                    >
                                        <Tabs variant="enclosed" bg="#4e4e4e" borderRadius={5} width="100%" height="100%" isFitted>
                                            <TabList borderColor="#ffffff" h="8%">
                                                {["Tree Map", "Pie Chart", "Other"].map((tabLabel, i) => (
                                                    <Tab
                                                        key={i}
                                                        as="h1"
                                                        fontWeight="semibold"
                                                        borderRadius={2}
                                                        borderWidth={3}
                                                        _selected={{ color: "#2b6cb0", borderColor: "#2b6cb0" }}
                                                        color="white"
                                                        _hover={{ color: "#95b0d8", borderColor: "#95b0d8" }}
                                                    >
                                                        {tabLabel}
                                                    </Tab>
                                                ))}
                                            </TabList>

                                            <TabPanels>
                                                <TabPanel shadow="bg" h="100%" p={6} justifyContent="center" alignItems="center">
                                                    <TreeMap />
                                                </TabPanel>
                                                <TabPanel shadow="bg" h="100%" w="100%" p={2} justifyContent="center" alignItems="center">
                                                    <PieChart />
                                                </TabPanel>
                                                <TabPanel shadow="bg" h="100%" p={2} justifyContent="center" alignItems="center"></TabPanel>
                                            </TabPanels>
                                        </Tabs>
                                    </Box>
                                </GraphDataProvider>
                            </Flex>
                        </TabPanel>
                    ))
                ) : (
                    <TabPanel>
                        <Text color="white">Please add a cloud service.</Text>
                    </TabPanel>
                )}
            </TabPanels>
        </Tabs>
    );
};

export default TabsComponent;
