import React, { createContext, useState, useContext } from "react";

const CloudContext = createContext(null);

export const useCloud = () => useContext(CloudContext);

export const CloudProvider = ({ children }) => {
  // Initialize cloudData as an array
  const [cloudData, setCloudData] = useState([]);

  // Update the function to add cloud service data to the array
  const addCloudService = (name, data) => {
    setCloudData((prev) => [
      ...prev,
      { cloud_name: name, cloud_data: data },
    ]);
  };

  return (
    <CloudContext.Provider value={{ cloudData, addCloudService }}>
      {children}
    </CloudContext.Provider>
  );
};
