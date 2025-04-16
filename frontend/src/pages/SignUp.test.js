import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import SignUp from './SignUp';
import '@testing-library/jest-dom';
import { BrowserRouter as Router, MemoryRouter } from 'react-router-dom';
import axios from 'axios';
import React from "react";

// Mock axios post request
jest.mock('axios');

// Mock the navigate function
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: jest.fn(),
}));

describe('SignUp Component', () => {
  const mockNavigate = jest.fn();

  beforeEach(() => {
    mockNavigate.mockClear();
    jest.clearAllMocks();
  });

  test('renders SignUp form', () => {
    render(
      <MemoryRouter>
        <SignUp />
      </MemoryRouter>
    );

    // Check if required fields and buttons are rendered
    expect(screen.getByLabelText(/Email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Password/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Confirm Password/i)).toBeInTheDocument();
    expect(screen.getByText(/Sign Up/i)).toBeInTheDocument();
    expect(screen.getByText(/Already have an account\?/i)).toBeInTheDocument();
  });

  test('handles user input for email, name, password, and confirm password', () => {
    render(
      <MemoryRouter>
        <SignUp />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByLabelText(/Email/i), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByLabelText(/Name/i), { target: { value: 'John Doe' } });
    fireEvent.change(screen.getByLabelText(/Password/i), { target: { value: 'Password123!' } });
    fireEvent.change(screen.getByLabelText(/Confirm Password/i), { target: { value: 'Password123!' } });

    // Check if the values are updated correctly
    expect(screen.getByLabelText(/Email/i).value).toBe('test@example.com');
    expect(screen.getByLabelText(/Name/i).value).toBe('John Doe');
    expect(screen.getByLabelText(/Password/i).value).toBe('Password123!');
    expect(screen.getByLabelText(/Confirm Password/i).value).toBe('Password123!');
  });

  test('shows password strength validation', () => {
    render(
      <MemoryRouter>
        <SignUp />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByLabelText(/Password/i), { target: { value: 'Password123!' } });

    // Check if the password strength validation rules are displayed
    expect(screen.getByText(/At least 8 characters/)).toBeInTheDocument();
    expect(screen.getByText(/At least one uppercase letter/)).toBeInTheDocument();
    expect(screen.getByText(/At least one lowercase letter/)).toBeInTheDocument();
    expect(screen.getByText(/At least one number/)).toBeInTheDocument();
    expect(screen.getByText(/At least one special character/)).toBeInTheDocument();
  });

  test('shows error message when passwords do not match', () => {
    render(
      <MemoryRouter>
        <SignUp />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByLabelText(/Password/i), { target: { value: 'Password123!' } });
    fireEvent.change(screen.getByLabelText(/Confirm Password/i), { target: { value: 'DifferentPassword!' } });

    // Check if error message is displayed
    expect(screen.getByText(/❌ Passwords do not match./)).toBeInTheDocument();
  });

  test('calls the API on successful sign up', async () => {
    const mockSuccessResponse = {
      status: 200,
      data: {
        success: true,
        access_token: 'mockAccessToken',
        refresh_token: 'mockRefreshToken',
      },
    };

    axios.post.mockResolvedValue(mockSuccessResponse);
    render(
      <MemoryRouter>
        <SignUp />
      </MemoryRouter>
    );

    // Fill in the form
    fireEvent.change(screen.getByLabelText(/Email/i), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByLabelText(/Name/i), { target: { value: 'John Doe' } });
    fireEvent.change(screen.getByLabelText(/Password/i), { target: { value: 'Password123!' } });
    fireEvent.change(screen.getByLabelText(/Confirm Password/i), { target: { value: 'Password123!' } });

    // Simulate form submission
    fireEvent.click(screen.getByText(/Sign Up/i));

    // Wait for API call and check if localStorage is updated
    await waitFor(() => expect(localStorage.setItem).toHaveBeenCalledWith('accessToken', 'mockAccessToken'));
    await waitFor(() => expect(localStorage.setItem).toHaveBeenCalledWith('refreshToken', 'mockRefreshToken'));
  });

  test('shows error message on failed sign up', async () => {
    const mockErrorResponse = {
      status: 500,
      data: { detail: 'Internal Server Error' },
    };

    axios.post.mockRejectedValue(mockErrorResponse);
    render(
      <MemoryRouter>
        <SignUp />
      </MemoryRouter>
    );

    // Fill in the form
    fireEvent.change(screen.getByLabelText(/Email/i), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByLabelText(/Name/i), { target: { value: 'John Doe' } });
    fireEvent.change(screen.getByLabelText(/Password/i), { target: { value: 'Password123!' } });
    fireEvent.change(screen.getByLabelText(/Confirm Password/i), { target: { value: 'Password123!' } });

    // Simulate form submission
    fireEvent.click(screen.getByText(/Sign Up/i));

    // Wait for the error message
    await waitFor(() => expect(screen.getByText(/❌ Error connecting to the server./)).toBeInTheDocument());
  });

  test('navigates to login page on "Log In" click', () => {
    render(
      <MemoryRouter>
        <SignUp />
      </MemoryRouter>
    );

    // Simulate click on "Log In" link
    fireEvent.click(screen.getByText(/Log In/i));

    // Check if navigate function was called with "/login"
    expect(mockNavigate).toHaveBeenCalledWith('/login');
  });
});
