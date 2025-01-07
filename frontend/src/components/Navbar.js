//function NavBar() {
//}

// components/Navbar.jsx
// components/Navbar.jsx
import { Box, VStack, Link, Text } from '@chakra-ui/react';
import { NavLink } from 'react-router-dom';

const Navbar = () => {
  return (
    <Box
        display={"flex"}
      as="nav"
      bg="#2e2e2e"
        color="white"
      w="20%" // Sidebar width
      h="100vh" // Full height
      position="fixed" // Fix to the left side of the screen
      p={4} // Padding inside the sidebar
    >
      <VStack spacing={4} align="stretch">
        <Text fontSize="xl" fontWeight="bold">Cloud Storage Manager</Text>

        {/* Add navigation links */}
        {/*<NavLink to="/main" style={({ isActive }) => ({ color: isActive ? "yellow" : "white" })}>*/}
        {/*  <Text>Dashboard</Text>*/}
        {/*</NavLink>*/}
        {/*<NavLink to="/profile" style={({ isActive }) => ({ color: isActive ? "yellow" : "white" })}>*/}
        {/*  <Text>Profile</Text>*/}
        {/*</NavLink>*/}
        {/*<NavLink to="/settings" style={({ isActive }) => ({ color: isActive ? "yellow" : "white" })}>*/}
        {/*  <Text>Settings</Text>*/}
        {/*</NavLink>*/}
        {/*<NavLink to="/logout" style={({ isActive }) => ({ color: isActive ? "yellow" : "white" })}>*/}
        {/*  <Text>Logout</Text>*/}
        {/*</NavLink>*/}
      </VStack>
    </Box>
  );
};

export default Navbar;

