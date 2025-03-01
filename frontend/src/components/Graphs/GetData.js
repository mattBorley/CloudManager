// Original flat data structure
const data = [
  { name: 'Group A', value: 400 },
  { name: 'Group B', value: 300 },
  { name: 'Group C', value: 300 },
  { name: 'Group D', value: 200 },
  { name: 'Group E', value: 20 },
  { name: 'Group F', value: 100 },
  { name: 'Group D', value: 500 },
];



const hierarchicalData = [
  {
    name: 'Category 1',
    children: data,
  },
];

export const sortDataByValue = (data) => {
  const minValue = Math.min(...data.map(d => d.value));
  const maxValue = Math.max(...data.map(d => d.value));

  const sortedData = [...data].sort((a, b) => b.value - a.value);

  return { sortedData, minValue, maxValue };
};

// Export both `data` and `hierarchicalData`
export { data, hierarchicalData };
