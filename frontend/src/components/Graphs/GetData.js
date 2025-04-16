import { createContext, useContext, useMemo } from "react";

// Create context for Graph data
const GraphDataContext = createContext();

// Function to process the data
const processData = (data) => {
  if (
    !data.storage ||
    data.storage.used_storage === undefined ||
    data.storage.total_storage === undefined ||
    !data.file_types
  ) {
    console.log("Missing required storage data or file_types, returning default structure.");
    return {
      hierarchicalData: [],
      usedStorage: 0,
      remainingStorage: 0,
      totalStorage: 0,
      file_types: [],
    };
  }

  const { used_storage, total_storage, remaining_storage } = data.storage;
  const { file_types, folder_structure } = data;

  // Recursive folder structure processor
  const processFolderStructure = (folders) => {
    return folders.map((folder) => {
      if (folder.type === "file") {
        return {
          name: folder.name,
          value: folder.size,
        };
      }

      if (folder.type === "folder") {
        const children = processFolderStructure(folder.children || []);
        return {
          name: folder.name,
          children,
          value: children.reduce((sum, child) => sum + (child.value || 0), 0),
        };
      }

      return {};
    });
  };

  const hierarchicalData = processFolderStructure(folder_structure || []);

  return {
    hierarchicalData,
    used_storage: used_storage,
    remaining_storage: remaining_storage,
    total_storage: total_storage,
    file_types: file_types || [],
  };
};

// GraphDataProvider Component
export const GraphDataProvider = ({ cloudData, children }) => {
  const processedData = useMemo(() => processData(cloudData), [cloudData]);

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
