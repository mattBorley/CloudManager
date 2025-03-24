import React, { createContext, useContext, useMemo } from "react";

const GraphDataContext = createContext();

const processStorageData = (storage) => {
  if (!storage || storage.used_storage === undefined || storage.total_storage === undefined) {
    return { sortedData: [], minValue: 0, maxValue: 0 };
  }

  const { used_storage, total_storage, remaining_storage } = storage;

  const availableStorage = remaining_storage !== undefined ? remaining_storage : total_storage - used_storage;

  const data = [
    { name: "Used Storage", value: used_storage },
    { name: "Available Storage", value: availableStorage },
  ];

  const sortedData = [...data].sort((a, b) => b.value - a.value);

  return {
    sortedData,
    minValue: Math.min(used_storage, availableStorage),
    maxValue: total_storage,
    used_storage,
    remaining_storage: availableStorage,
  };
};

export const GraphDataProvider = ({ cloudData, children }) => {
  const processedData = useMemo(() => processStorageData(cloudData), [cloudData]);

  return (
    <GraphDataContext.Provider value={processedData}>
      {children}
    </GraphDataContext.Provider>
  );
};

// Custom hook to access the context
export const useGraphData = () => useContext(GraphDataContext);
