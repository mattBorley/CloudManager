// components/Layout.jsx
import { Box } from '@chakra-ui/react';
import Navbar from './Navbar';

const Layout = ({ children }) => {
  return (
    <Box>
      <Navbar />
      <Box as="main" >
        {children}
      </Box>
    </Box>
  );
};

export default Layout;
