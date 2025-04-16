import React from "react";
import { Treemap, ResponsiveContainer, Tooltip } from "recharts";
import { useGraphData } from "./GetData";

const TreeMap = () => {
  const { hierarchicalData, total_storage = 1 } = useGraphData(); // Default to prevent 0 or undefined

  if (!hierarchicalData || hierarchicalData.length === 0) {
    return <div>No data available</div>;
  }

  const MIN_USED_PERCENTAGE = 0.05; // Minimum 5% size for used storage
  const usedSize = Math.max(total_storage * MIN_USED_PERCENTAGE, 0); // Prevent negatives

  const hierarchicalDataWithStorage = [
    {
      name: "Storage",
      children: hierarchicalData,
      value: total_storage,
    },
  ];

  return (
    <ResponsiveContainer width="100%" height={550}>
      <Treemap
        data={hierarchicalDataWithStorage}
        dataKey="value"
        nameKey="name"
        aspectRatio={1}
        stroke="#fff"
        fill="#2e2e2e"
        label={({ name }) => name}
        isAnimationActive={false}
      />
      <Tooltip
        content={({ payload }) => {
          if (payload && payload.length > 0) {
            const data = payload[0].payload;
            return (
              <div
                style={{
                  backgroundColor: "#fff",
                  color: "#2e2e2e",
                  border: "1px solid #ccc",
                  padding: "10px",
                  fontSize: "14px",
                }}
              >
                <strong>{data.name}</strong>: {data.value.toLocaleString()} bytes
              </div>
            );
          }
          return null;
        }}
      />
    </ResponsiveContainer>
  );
};

export default TreeMap;
