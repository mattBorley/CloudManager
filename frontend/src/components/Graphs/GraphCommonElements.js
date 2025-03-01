export const interpolateColor = (value, minValue, maxValue) => {
  const normalizedValue = (value - minValue) / (maxValue - minValue);



  if (normalizedValue <= 0.5) {
    const r = 0; // Red stays at 0
    const g = Math.floor(255 * (normalizedValue * 2)); // Green increases from 0 to 255
    const b = 255; // Blue stays at 255
    return `rgb(${r}, ${g}, ${b})`;
  } else {
    const r = Math.floor(255 * ((normalizedValue - 0.5) * 2)); // Red increases from 0 to 255
    const g = Math.floor(255 * (2 - normalizedValue * 2)); // Green decreases from 255 to 0
    const b = 0; // Blue stays at 0
    return `rgb(${r}, ${g}, ${b})`;
  }
};

