import React, {createContext, useContext, useMemo} from "react";

// Create context for Graph data
const GraphDataContext = createContext();

// Function to process the data
const processData = (data) => {

  // Check if the required storage data is available
  if (!data.storage || data.storage.used_storage === undefined || data.storage.total_storage === undefined || !data.file_types) {
    console.log("Missing required storage data or file_types, returning default structure.");
    return {
      sortedData: [],
      minValue: 0,
      maxValue: 0,
      file_types: [],
    };
  }

  // Destructure storage data and file types from cloudData
  const { used_storage, total_storage, remaining_storage } = data.storage;
  const { file_types } = data;


  // Calculate available storage (remaining_storage or the difference between total and used)
  const availableStorage = remaining_storage !== undefined ? remaining_storage : total_storage - used_storage;


  // Process storage data into a more usable format for charts
  const processed_storage = [
    { name: "Used Storage", value: used_storage },
    { name: "Available Storage", value: availableStorage },
  ];


  // Sort the storage data in descending order based on value
  const sortedData = [...processed_storage].sort((a, b) => b.value - a.value);


  return {
    sortedData,
    minValue: Math.min(used_storage, availableStorage),
    maxValue: total_storage,
    used_storage,
    remaining_storage: availableStorage,
    file_types: file_types || [],
  };
};

// GraphDataProvider Component
export const GraphDataProvider = ({ cloudData, children }) => {

  // Use useMemo to process data and memoize the result
  const processedData = useMemo(() => {
    return processData(cloudData);
  }, [cloudData]);


  return (
    <GraphDataContext.Provider value={processedData}>
      {children}
    </GraphDataContext.Provider>
  );
};

// Custom hook to access the context
export const useGraphData = () => {
  return useContext(GraphDataContext);
};
