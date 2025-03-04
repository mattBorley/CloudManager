import React, { createContext, useState, useContext } from "react";

const CloudContext = createContext(null);

export const useCloud = () => useContext(CloudContext);

export const CloudProvider = ({ children }) => {
  const [cloudData, setCloudData] = useState([]);

  const addCloudService = (name, data) => {
    setCloudData((prev) => [...prev, data]);
  };

  return (
    <CloudContext.Provider value={{ cloudData, addCloudService }}>
      {children}
    </CloudContext.Provider>
  );
};
