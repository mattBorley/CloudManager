import '../styling/Main.css';
//import DataFetcher from "./DataFetcher";
import { Box, Button, Heading, Card, Flex} from "@chakra-ui/react";


function Main() {
  return (
    <Flex height="100vh">
      {/* Main content area to the right of the navbar */}

        <Card
          className={"Background-Box"}
          minH="100%"
          w="80%"
          p={4}
          display="flex"
          alignItems="center"
          flexDir="column"
          borderRadius="0"
          ml="250px"
        >
          <Heading as="h1" size="2xl" mb={4}>
            Welcome to React with Chakra UI
          </Heading>

          <Button colorScheme="teal" size="lg" onClick={() => alert('Button clicked!')}>
            Click Me
          </Button>
        </Card>

    </Flex>
  );
}

export default Main;