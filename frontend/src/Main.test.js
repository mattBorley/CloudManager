import { render, screen } from '@testing-library/react';
import Main from './pages/Main';

test('renders Cloud Storage Manager heading', () => {
  render(<Main />);
  const headingElement = screen.getByText(/Cloud Storage Manager/i);
  expect(headingElement).toBeInTheDocument();
});
