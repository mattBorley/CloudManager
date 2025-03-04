import React, {useEffect} from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';
import { useGraphData } from "./GetData";
import { interpolateColor } from "./GraphCommonElements";

const MyPieChart = () => {
  const { storageUsed, storageAvailable } = useGraphData();

  const chartData = [
    { name: 'Used Storage', value: storageUsed },
    { name: 'Available Storage', value: storageAvailable },
  ];
    useEffect(() => {
        console.log(storageAvailable)
    }, []);

  const minValue = 0;
  const maxValue = storageUsed + storageAvailable;

  const colors = ["#FF5733", "#33FF57"];

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
            fill={colors[index]}
            stroke={interpolateColor(entry.value, minValue, maxValue)}
            strokeWidth={4}
            strokeLinejoin="round"
          />
        ))}
      </Pie>

      <Tooltip />

      <Legend
        formatter={(value, entry) => (
          <span style={{ color: 'white', fontSize: 14, fontWeight: 'bold' }}>
            {value}
          </span>
        )}
      />

      <text
        x="50%"
        y="48%"
        textAnchor="middle"
        dominantBaseline="middle"
        style={{
          fill: 'white',
          fontSize: 14,
          fontWeight: 'bold',
        }}
      >
        Storage Usage
      </text>
    </PieChart>
  );
};

export default MyPieChart;
