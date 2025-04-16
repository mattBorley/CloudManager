import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Login from './Login';
import '@testing-library/jest-dom'; // for the "toBeInTheDocument" matcher
import { BrowserRouter as Router } from 'react-router-dom';
import axios from 'axios';

// Mocking the axios post method
jest.mock('axios');

describe('Login Component', () => {
  test('renders login form with email, password inputs, and buttons', () => {
    render(
      <Router>
        <Login />
      </Router>
    );

    // Check if elements are rendered
    expect(screen.getByLabelText(/Email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Password/i)).toBeInTheDocument();
    expect(screen.getByText(/Log In/i)).toBeInTheDocument();
    expect(screen.getByText(/Sign Up/i)).toBeInTheDocument();
    expect(screen.getByText(/Recover Here/i)).toBeInTheDocument();
  });

  test('shows error message for invalid email format', () => {
    render(
      <Router>
        <Login />
      </Router>
    );

    const emailInput = screen.getByLabelText(/Email/i);
    const passwordInput = screen.getByLabelText(/Password/i);
    const loginButton = screen.getByText(/Log In/i);

    // Simulate entering invalid email
    fireEvent.change(emailInput, { target: { value: 'invalid-email' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });

    // Click login button
    fireEvent.click(loginButton);

    // Check for error message
    expect(screen.getByText(/Please enter valid email./i)).toBeInTheDocument();
  });

  test('shows error message for empty email and password fields', () => {
    render(
      <Router>
        <Login />
      </Router>
    );

    const loginButton = screen.getByText(/Log In/i);

    // Simulate clicking the login button without filling in any input fields
    fireEvent.click(loginButton);

    // Check for error message
    expect(screen.getByText(/Please enter your credentials./i)).toBeInTheDocument();
  });

  test('calls the login API with correct credentials', async () => {
    render(
      <Router>
        <Login />
      </Router>
    );

    const emailInput = screen.getByLabelText(/Email/i);
    const passwordInput = screen.getByLabelText(/Password/i);
    const loginButton = screen.getByText(/Log In/i);

    const mockResponse = {
      data: { success: true, access_token: 'mockAccessToken', refresh_token: 'mockRefreshToken' },
      status: 200,
    };

    // Mock the axios post response
    axios.post.mockResolvedValue(mockResponse);

    // Simulate entering valid credentials
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'password123' } });

    // Click login button
    fireEvent.click(loginButton);

    // Wait for the login API call to complete
    await waitFor(() => {
      expect(axios.post).toHaveBeenCalledWith(
        'http://localhost:5000/api/users/login', // Adjust this URL based on your backend setup
        { email: 'test@example.com', password: 'password123' },
        { headers: { 'Content-Type': 'application/json' }, withCredentials: true }
      );
    });

    // Check if the login was successful
    expect(localStorage.getItem('accessToken')).toBe('mockAccessToken');
    expect(localStorage.getItem('refreshToken')).toBe('mockRefreshToken');
  });

  test('handles API error and displays appropriate error message', async () => {
    render(
      <Router>
        <Login />
      </Router>
    );

    const emailInput = screen.getByLabelText(/Email/i);
    const passwordInput = screen.getByLabelText(/Password/i);
    const loginButton = screen.getByText(/Log In/i);

    const mockErrorResponse = {
      response: { status: 400, data: { detail: 'Invalid credentials' } },
    };

    // Mock the axios post response for error
    axios.post.mockRejectedValue(mockErrorResponse);

    // Simulate entering valid credentials
    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'wrongpassword' } });

    // Click login button
    fireEvent.click(loginButton);

    // Check for error message after failed login
    await waitFor(() => {
      expect(screen.getByText(/Invalid credentials/i)).toBeInTheDocument();
    });
  });

  test('toggles password visibility on click', () => {
    render(
      <Router>
        <Login />
      </Router>
    );

    const passwordInput = screen.getByLabelText(/Password/i);
    const toggleButton = screen.getByText(/Show/i);

    // Initially password input type should be "password"
    expect(passwordInput.type).toBe('password');

    // Simulate toggling the password visibility
    fireEvent.click(toggleButton);

    // After clicking, the input type should be "text"
    expect(passwordInput.type).toBe('text');
    expect(toggleButton.textContent).toBe('Hide');
  });
});
