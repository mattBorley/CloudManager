// SignUp.test.js
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import SignUp from './SignUp';
import '@testing-library/jest-dom';
import { MemoryRouter } from 'react-router-dom';
import axios from 'axios';
import React from "react";

// Mock axios post request
jest.mock('axios');

// Mock the navigate function
const mockNavigate = jest.fn();
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useNavigate: () => mockNavigate,
}));

describe('SignUp Component', () => {
  beforeEach(() => {
    mockNavigate.mockClear();
    jest.clearAllMocks();
    jest.spyOn(Storage.prototype, 'setItem');
  });

  test('renders SignUp form', () => {
    render(
      <MemoryRouter>
        <SignUp />
      </MemoryRouter>
    );

    expect(screen.getByLabelText(/Email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Name/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Enter your password')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Re-enter your password')).toBeInTheDocument();
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
    fireEvent.change(screen.getByPlaceholderText('Enter your password'), { target: { value: 'Password123!' } });
    fireEvent.change(screen.getByPlaceholderText('Re-enter your password'), { target: { value: 'Password123!' } });


    expect(screen.getByLabelText(/Email/i).value).toBe('test@example.com');
    expect(screen.getByLabelText(/Name/i).value).toBe('John Doe');
    expect(screen.getByPlaceholderText('Enter your password').value).toBe('Password123!');
    expect(screen.getByPlaceholderText('Re-enter your password').value).toBe('Password123!');
  });

  test('shows password strength validation', () => {
    render(
      <MemoryRouter>
        <SignUp />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByPlaceholderText('Enter your password'), { target: { value: 'Password123!' } });

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

    fireEvent.change(screen.getByPlaceholderText('Enter your password'), { target: { value: 'Password123!' } });
    fireEvent.change(screen.getByPlaceholderText('Re-enter your password'), { target: { value: 'DifferentPassword!' } });

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

    fireEvent.change(screen.getByLabelText(/Email/i), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByLabelText(/Name/i), { target: { value: 'John Doe' } });
    fireEvent.change(screen.getByPlaceholderText('Enter your password'), { target: { value: 'Password123!' } });
    fireEvent.change(screen.getByPlaceholderText('Re-enter your password'), { target: { value: 'Password123!' } });

    fireEvent.click(screen.getByRole('button', { name: /sign up/i }));

    await waitFor(() => expect(localStorage.setItem).toHaveBeenCalledWith('accessToken', 'mockAccessToken'));
    await waitFor(() => expect(localStorage.setItem).toHaveBeenCalledWith('refreshToken', 'mockRefreshToken'));
  });

  test('shows error message on failed sign up', async () => {
    const mockErrorResponse = {
      response: {
        status: 500,
        data: { detail: 'Internal Server Error' },
      },
    };

    axios.post.mockRejectedValue(mockErrorResponse);

    render(
      <MemoryRouter>
        <SignUp />
      </MemoryRouter>
    );

    fireEvent.change(screen.getByLabelText(/Email/i), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByLabelText(/Name/i), { target: { value: 'John Doe' } });
    fireEvent.change(screen.getByPlaceholderText('Enter your password'), { target: { value: 'Password123!' } });
    fireEvent.change(screen.getByPlaceholderText('Re-enter your password'), { target: { value: 'Password123!' } });

    fireEvent.click(screen.getByRole('button', { name: /sign up/i }));

    await waitFor(() => expect(screen.getByText(/❌ Error connecting to the server./)).toBeInTheDocument());
  });

  test('navigates to login page on "Log In" click', () => {
    render(
      <MemoryRouter>
        <SignUp />
      </MemoryRouter>
    );

    fireEvent.click(screen.getByText(/Log In/i));
    expect(mockNavigate).toHaveBeenCalledWith('/login');
  });
});
