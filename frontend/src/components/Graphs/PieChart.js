import React, { useEffect } from "react";
import { PieChart, Pie, Cell, Tooltip, Legend } from "recharts";
import { useGraphData } from "./GetData";  // Import custom hook for context
import { interpolateColor } from "./GraphCommonElements";
import { formatStorageSize } from "../Tabs";  // Assuming this is a custom function for color interpolation

const MyPieChart = () => {
  const { used_storage, remaining_storage } = useGraphData();

  useEffect(() => {
    console.log("Used Storage:", used_storage);
    console.log("Used Storage:", formatStorageSize(used_storage));
    console.log("Available Storage:", remaining_storage);
    console.log("Available Storage:", formatStorageSize(remaining_storage));
  }, [used_storage, remaining_storage]);  // Run effect whenever the data changes

  const chartData = [
    { name: "Used Storage", value: used_storage },
    { name: "Available Storage", value: remaining_storage },
  ];

  const minValue = 0;
  const maxValue = used_storage + remaining_storage;

  return (
    <PieChart width={750} height={550}>
      <Pie
        data={chartData}
        dataKey="value"
        nameKey="name"
        paddingAngle={4}
        outerRadius={150}
        innerRadius={100}
        labelLine={false}
        label={false}
      >
        {chartData.map((entry, index) => {
          const strokeColor = interpolateColor(entry.value, minValue, maxValue); // Calculate stroke color
          return (
            <Cell
              key={`cell-${index}`}
              fill={"#2e2e2e"}  // Fill color of the slice
              stroke={strokeColor} // Stroke (border) color
              strokeWidth={4}
              strokeLinejoin="round"
            />
          );
        })}
      </Pie>

      <Tooltip
        content={({ active, payload }) => {
          if (active && payload && payload.length) {
            const data = payload[0];
            return (
              <div
                style={{
                  background: "#333",
                  padding: "8px 12px",
                  borderRadius: 6,
                  color: "white",
                  fontWeight: "bold",
                  fontSize: 14,
                  boxShadow: "0 2px 8px rgba(0,0,0,0.5)",
                }}
              >
                <div>{data.name}</div>
                <div>{formatStorageSize(data.value)}</div>
              </div>
            );
          }
          return null;
        }}
      />

      <Legend
        iconType="circle"  // Change the legend icon type to a circle
        formatter={(value, entry) => (
          <span
            style={{
              color: "white", // Keep text color white
              fontSize: 14,
              fontWeight: "bold",
            }}
          >
            {value}
          </span>
        )}
        payload={chartData.map((entry, index) => {
          const strokeColor = interpolateColor(entry.value, minValue, maxValue); // Get the stroke color
          return {
            value: entry.name,
            type: "circle",
            color: strokeColor, // Use stroke color for the legend
          };
        })}
      />

      <text
        x="50%"
        y="48%"
        textAnchor="middle"
        dominantBaseline="middle"
        style={{
          fill: "white",
          fontSize: 14,
          fontWeight: "bold",
        }}
      >
        Storage Usage
      </text>
    </PieChart>
  );
};

export default MyPieChart;
