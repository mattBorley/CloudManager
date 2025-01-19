import { screen } from '@testing-library/react';
import './index';

test('renders without crashing', () => {
  const element = screen.getByTestId('app-root');
  expect(element).toBeInTheDocument();
});
