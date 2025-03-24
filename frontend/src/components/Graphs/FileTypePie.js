import React, { useEffect } from "react";
import { PieChart, Pie, Cell, Tooltip, Legend } from "recharts";
import { useGraphData } from "./GetData";  // Import custom hook for context
import { interpolateColor } from "./GraphCommonElements";  // Assuming this is a custom function for color interpolation

const FileTypesPieChart = () => {
  const { file_types } = useGraphData(); // Assuming file_types is part of cloudData

  useEffect(() => {
    console.log("File Types:", file_types); // Check the data coming from context
  }, [file_types]);

  // Map the file types data to the chart format
  const chartData = file_types.map((fileType) => ({
    name: fileType.type,
    value: fileType.size,
  }));

  const minValue = 0;
  const maxValue = chartData.reduce((acc, entry) => acc + entry.value, 0);

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
        {chartData.map((entry, index) => (
          <Cell
            key={`cell-${index}`}
            fill={"#2e2e2e"}  // Fill color of the slice
            stroke={interpolateColor(entry.value, minValue, maxValue)} // Stroke (border) color
            strokeWidth={4}
            strokeLinejoin="round"
          />
        ))}
      </Pie>

      <Tooltip />

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
        payload={chartData.map((entry, index) => ({
          value: entry.name,
          type: "circle",
          color: interpolateColor(entry.value, minValue, maxValue),  // Set the color to the stroke color
        }))}
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
        File Types Distribution
      </text>
    </PieChart>
  );
};

export default FileTypesPieChart;
