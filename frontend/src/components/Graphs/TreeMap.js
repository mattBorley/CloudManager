import React from "react";
import { Treemap, ResponsiveContainer, Tooltip, Legend } from "recharts";
import { useGraphData } from "./GetData";

const TreemapChart = () => {
  const { sortedData, totalStorage = 1 } = useGraphData(); // Default to prevent 0 or undefined

  console.log("Sorted Data for Treemap:", sortedData);
  console.log("Total Storage:", totalStorage);

  if (!sortedData || sortedData.length === 0 || totalStorage <= 0) {
    return <div>No data available</div>;
  }

  const usedStorage = sortedData.reduce((acc, item) => acc + item.value, 0);
  console.log("Used Storage:", usedStorage);

  const MIN_USED_PERCENTAGE = 0.05; // Minimum 5% size for used storage
  const usedSize = Math.max(usedStorage, totalStorage * MIN_USED_PERCENTAGE);
  const remainingSize = Math.max(totalStorage - usedSize, 0); // Prevent negatives

  console.log("Used Size:", usedSize);
  console.log("Remaining Size:", remainingSize);

  const hierarchicalData = [
    {
      name: "Storage",
      children: [
        { name: "Storage Used", value: usedSize, fill: "#ff6666" },
        { name: "Remaining Storage", value: remainingSize, fill: "#66cc66" },
      ],
    },
  ];

  return (
    <ResponsiveContainer width="100%" height={550}>
      <Treemap
        data={hierarchicalData}
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

export default TreemapChart;
