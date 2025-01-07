import '../styling/Main.css';
//import DataFetcher from "./DataFetcher";
import { Button, Heading, Card, Flex} from "@chakra-ui/react";
import {useNavigate} from "react-router-dom";

function Main() {
    const navigate = useNavigate()

    const toLoginPage = () => {
        navigate("/login")
    }
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

              <Button colorScheme="teal" size="lg" onClick={toLoginPage}>
                Log Out
              </Button>
            </Card>

        </Flex>
    );
}

export default Main;