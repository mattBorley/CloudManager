import React from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';
import {data, sortDataByValue} from "./GetData";
import { interpolateColor } from "./GraphCommonElements";

// Function to sort the data by value and calculate min and max values


const MyPieChart = ({ width, height }) => {
  const { sortedData, minValue, maxValue } = sortDataByValue(data);

  const renderCustomLegend = (props) => {
    const { payload } = props;

    return (
      <ul style={{
        listStyleType: 'none',
        padding: 0,
        margin: 0,
        display: 'flex',
        justifyContent: 'center',
        flexWrap: 'wrap'
      }}>
        {payload.map((entry, index) => (
          <li
            key={`legend-item-${index}`}
            style={{
              display: 'flex',
              alignItems: 'center',
              marginRight: 15,
              marginBottom: 10,
              color: 'white',
            }}
          >
            <div
              style={{
                width: 20,
                height: 20,
                backgroundColor: entry.payload.stroke,
                marginRight: 8,
              }}
            />
            <span style={{ color: 'white', fontSize: 14, fontWeight: 'bold' }}>
              {entry.payload.name}
            </span>
          </li>
        ))}
      </ul>
    );
  };

  return (
    <PieChart width={width} height={height}>
      <Pie
        data={sortedData}  // Use sorted data here
        dataKey="value"
        nameKey="name"
        paddingAngle={4}
        outerRadius={150}
        innerRadius={100}
        fill="#fff"
        labelLine={false} // Remove leader lines
        label={false} // Disable the labels entirely
      >
        {sortedData.map((entry, index) => {
          // Get the color based on the value
          const borderColor = interpolateColor(entry.value, minValue, maxValue);

          return (
            <Cell
              key={`cell-${index}`}
              fill="#2e2e2e"
              stroke={borderColor}
              strokeWidth={4}
              strokeLinejoin="round" // Ensure clean borders
            />
          );
        })}
      </Pie>

      <Tooltip />

      <Legend content={renderCustomLegend} />

      <text
        x="50%"
        y="48%"
        textAnchor="middle"
        dominantBaseline="middle"
        style={{
          fill: 'white', // Ensure central text is white
          fontSize: 14, // Adjust font size for central text
          fontWeight: 'bold', // Optional: Make the text bold
        }}
      >
        Pie Chart Title or Description
      </text>
    </PieChart>
  );
};

export default MyPieChart;
