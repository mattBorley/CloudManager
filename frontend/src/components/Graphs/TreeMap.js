import React from 'react';
import { Treemap, ResponsiveContainer, Tooltip } from 'recharts';
import {hierarchicalData} from "./GetData";

const TreemapChart = () => {
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
      >
        {/* Tooltip component to show data on hover */}
        <Tooltip
          contentStyle={{
            backgroundColor: '#fff', // Tooltip background color
            color: '#2e2e2e', // Tooltip text color
            border: '1px solid #ccc', // Border style
          }}
        />
      </Treemap>
    </ResponsiveContainer>
  );
};

export default TreemapChart;
