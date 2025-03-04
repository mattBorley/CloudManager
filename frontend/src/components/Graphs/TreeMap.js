import React from 'react';
import { Treemap, ResponsiveContainer, Tooltip } from 'recharts';
import { useGraphData } from "./GetData";

const TreemapChart = () => {
  const { storageUsed, storageAvailable } = useGraphData();

  const hierarchicalData = [
    {
      name: "Storage",
      children: [
        { name: "Used Storage", value: storageUsed },
        { name: "Available Storage", value: storageAvailable },
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
        label={({ name, value }) => `${name}: ${value}`}
        isAnimationActive={false}
      />
      <Tooltip
        contentStyle={{
          backgroundColor: '#fff',
          color: '#2e2e2e',
          border: '1px solid #ccc',
        }}
      />
    </ResponsiveContainer>
  );
};

export default TreemapChart;
