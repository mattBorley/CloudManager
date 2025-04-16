// jest.config.js
module.exports = {
  testEnvironment: "jsdom",
  setupFilesAfterEnv: ["<rootDir>/src/setupTests.js"],
  moduleNameMapper: {
    "\\.(css|less|scss|sass)$": "identity-obj-proxy",
    "\\.(webp|jpg|jpeg|png|gif|svg)$": "<rootDir>/src/__mocks__/fileMock.js",
    "^react-simple-maps$": "<rootDir>/src/__mocks__/react-simple-maps.js",
  },
  transform: {
    "^.+\\.[jt]sx?$": "babel-jest",
  },
  transformIgnorePatterns: [
    "node_modules/(?!(d3-scale|axios|@chakra-ui|@emotion|framer-motion)/)"
  ],  // Include d3-scale explicitly
};
