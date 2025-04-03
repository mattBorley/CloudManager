import React, { useEffect } from "react";
import { PieChart, Pie, Cell, Tooltip, Legend } from "recharts";
import { useGraphData } from "./GetData";  // Import custom hook for context
import { scaleSequential } from "d3-scale"; // Import d3-scale for color interpolation
import { interpolateViridis } from "d3-scale-chromatic";  // Color interpolation from d3

const FileTypePie = () => {
  const { file_types } = useGraphData();

  useEffect(() => {
    console.log("File types: ", file_types);
  }, [file_types]);

  // Prepare chart data from the file_types object
  const chartData = Object.entries(file_types).map(([extension, count]) => ({
    name: extension,
    value: count,
  }));

  // Check if chartData has diverse values
  console.log("Chart Data: ", chartData);

  const minValue = Math.min(...chartData.map(entry => entry.value));
  const maxValue = Math.max(...chartData.map(entry => entry.value));

  // Adjust the domain to prevent identical colors
  const adjustedMin = minValue === maxValue ? minValue - 1 : minValue;
  const adjustedMax = maxValue;

  // Create a dynamic color scale
  const colorScale = scaleSequential(interpolateViridis).domain([adjustedMin, adjustedMax]);

  // Fallback color palette
  const colorPalette = ["#FF6347", "#2e8b57", "#4682b4", "#FFD700", "#8A2BE2", "#00CED1", "#DC143C", "#7FFF00"];

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
          const dynamicColor = minValue === maxValue
            ? colorPalette[index % colorPalette.length]  // Use fallback palette if values are identical
            : colorScale(entry.value);  // Otherwise, use dynamic scale

          return (
            <Cell
              key={`cell-${index}`}
              fill={dynamicColor}
              stroke={dynamicColor}
              strokeWidth={4}
              strokeLinejoin="round"
            />
          );
        })}
      </Pie>

      <Legend
        iconType="circle"
        formatter={(value) => (
          <span
            style={{
              color: "white",
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
          color: minValue === maxValue
            ? colorPalette[index % colorPalette.length]
            : colorScale(entry.value),
        }))}
      />

      <Tooltip formatter={(value, name) => [value, name]} />

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
        File Type Distribution
      </text>
    </PieChart>
  );
};

export default FileTypePie;
