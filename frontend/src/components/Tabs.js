import { Box, Flex, Tab, TabList, TabPanel, TabPanels, Tabs } from "@chakra-ui/react";
import React from "react";
import TreeMap from "./Graphs/TreeMap";
import PieChart from "./Graphs/PieChart";

const TabsComponent = ({ cloudData }) => {
  const tabData = cloudData.map((cloudService) => ({
    label: cloudService.cloud_name,
    content: cloudService.cloud_data
  }));

  return (
    <Tabs
      variant={"enclosed"}
      bg={"#4e4e4e"}
      borderRadius={5}
      width={"100%"}
      height={"100%"}
      isFitted={true}
    >
      <TabList borderColor={"#fffff"} h={"8%"}>
        {tabData.length > 0 ? (
          tabData.map((tab, index) => (
            <Tab
              key={index}
              as={"h1"}
              fontWeight={"semibold"}
              borderRadius={2}
              borderWidth={3}
              _selected={{
                color: "#2b6cb0",
                borderColor: "#2b6cb0"
              }}
              color={"white"}
              _hover={{
                color: "#95b0d8",
                borderColor: "#95b0d8"
              }}
            >
              {tab.label}
            </Tab>
          ))
        ) : (
          <Tab
            as={"h1"}
            fontWeight={"semibold"}
            borderRadius={2}
            borderWidth={3}
            isDisabled={true}
            _disabled={{ cursor: "default" }}
            borderColor={"#ffffff"}
            _selected={{
              borderColor: "#ffffff"
            }}
          >
            No Tabs Available
          </Tab>
        )}
      </TabList>

      <TabPanels borderColor={"#2e2e2e"} h={"92%"}>
        {tabData.length > 0 ? (
          tabData.map((tab, index) => (
            <TabPanel key={index} shadow={"bg"} h={"100%"} p={2}>
              <Flex
                w={"100%"}
                h={"100%"}
                justifyContent={"space-between"}
                alignItems={"center"}
              >
                <Box
                  bg={"#4e4e4e"}
                  w={"30%"}
                  h={"98%"}
                  p={4}
                  borderRadius={5}
                  overflowY="auto"
                >
                  {tab.content && tab.content.length > 0 ? (
                    <>
                      <p className="title">Storage Information:</p>
                      <div className="row">
                        <p className="label">Storage used:</p>
                        <p className="value">{tab.content[0]}</p>
                      </div>
                      <div className="row">
                        <p className="label">Capacity:</p>
                        <p className="value">{tab.content[1]}</p>
                      </div>
                      <div className="row">
                        <p className="label">Remaining Storage:</p>
                        <p className="value">{tab.content[2]}</p>
                      </div>
                      <div className="row">
                        <p className="label">Number of files:</p>
                        <p className="value">{tab.content[3]}</p>
                      </div>
                      <div className="row">
                        <p className="label">Largest folder:</p>
                        <p className="value">{tab.content[4]}</p>
                      </div>
                      <div className="row">
                        <p className="label">Number of duplicates:</p>
                        <p className="value">{tab.content[5]}</p>
                      </div>
                      <div className="row">
                        <p className="label">Storage used by duplicates:</p>
                        <p className="value">{tab.content[6]}</p>
                      </div>
                      <div className="row">
                        <p className="label">Largest File:</p>
                        <p className="value">{tab.content[7]}</p>
                      </div>
                      <div className="row">
                        <p className="label">Oldest File:</p>
                        <p className="value">{tab.content[8]}</p>
                      </div>
                      <div className="row">
                        <p className="label">Last Synced:</p>
                        <p className="value">{tab.content[9]}</p>
                      </div>
                    </>
                  ) : (
                    <p>No content available for this tab.</p>
                  )}
                </Box>

                <Box
                  bg={"#2e2e2e"}
                  w={"68%"}
                  h={"98%"}
                  p={4}
                  borderRadius={5}
                  shadow="md"
                  display="flex"
                  flexDir="column"
                  justifyContent="center"
                  alignItems="center"
                >
                  <Tabs
                    variant={"enclosed"}
                    bg={"#4e4e4e"}
                    borderRadius={5}
                    width={"100%"}
                    height={"100%"}
                    isFitted={true}
                  >
                    <TabList borderColor={"#fffff"} h={"8%"}>
                      <Tab
                        as={"h1"}
                        fontWeight={"semibold"}
                        borderRadius={2}
                        borderWidth={3}
                        _selected={{
                          color: "#2b6cb0",
                          borderColor: "#2b6cb0"
                        }}
                        color={"white"}
                        _hover={{
                          color: "#95b0d8",
                          borderColor: "#95b0d8"
                        }}
                      >
                        Tree Map
                      </Tab>
                      <Tab
                        as={"h1"}
                        fontWeight={"semibold"}
                        borderRadius={2}
                        borderWidth={3}
                        _selected={{
                          color: "#2b6cb0",
                          borderColor: "#2b6cb0"
                        }}
                        color={"white"}
                        _hover={{
                          color: "#95b0d8",
                          borderColor: "#95b0d8"
                        }}
                      >
                        Pie Chart
                      </Tab>
                      <Tab
                        as={"h1"}
                        fontWeight={"semibold"}
                        borderRadius={2}
                        borderWidth={3}
                        _selected={{
                          color: "#2b6cb0",
                          borderColor: "#2b6cb0"
                        }}
                        color={"white"}
                        _hover={{
                          color: "#95b0d8",
                          borderColor: "#95b0d8"
                        }}
                      >
                        Other
                      </Tab>
                    </TabList>

                    <TabPanels>
                      <TabPanel
                        shadow={"bg"}
                        h={"100%"}
                        p={6}
                        justifyContent={"center"}
                        alignItems={"center"}
                      >
                        <TreeMap />
                      </TabPanel>
                      <TabPanel
                        shadow={"bg"}
                        h={"100%"}
                        w={"100%"}
                        p={2}
                        justifyContent={"center"}
                        alignItems={"center"}
                      >
                        <PieChart width={750} height={525} />
                      </TabPanel>
                      <TabPanel
                        shadow={"bg"}
                        h={"100%"}
                        p={2}
                        justifyContent={"center"}
                        alignItems={"center"}
                      >
                      </TabPanel>
                    </TabPanels>
                  </Tabs>
                </Box>
              </Flex>
            </TabPanel>
          ))
        ) : (
          <TabPanel>
            <p>Please add a cloud service.</p>
          </TabPanel>
        )}
      </TabPanels>
    </Tabs>
  );
};

export default TabsComponent;
