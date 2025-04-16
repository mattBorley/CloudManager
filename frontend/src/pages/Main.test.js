import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Main from './Main';
import '@testing-library/jest-dom'; // for the "toBeInTheDocument" matcher
import { BrowserRouter as Router, MemoryRouter } from 'react-router-dom';
import axios from 'axios';
import { getAccessToken } from '../utils/Token_Checks';

// Mocking the axios GET method
jest.mock('axios');

// Mocking the getAccessToken utility function
jest.mock('../utils/Token_Checks', () => ({
  getAccessToken: jest.fn(),
}));

// Mocking components that are imported in the Main component
jest.mock('../components/CloudList', () => ({
  __esModule: true,
  default: ({ cloudList }) => (
    <div>{cloudList.length > 0 ? cloudList.join(', ') : 'No clouds available'}</div>
  ),
}));

jest.mock('../components/Tabs', () => ({
  __esModule: true,
  default: ({ cloudData }) => <div>{cloudData.length > 0 ? 'Tabs rendered' : 'No cloud data'}</div>,
}));

describe('Main Component', () => {
  beforeEach(() => {
    // Clear any mock implementation before each test
    axios.get.mockClear();
    getAccessToken.mockClear();
  });

  test('renders main page with title, sidebar, and buttons', () => {
    render(
      <MemoryRouter>
        <Main />
      </MemoryRouter>
    );

    // Check if elements are rendered correctly
    expect(screen.getByText(/Cloud Storage Manager/i)).toBeInTheDocument();
    expect(screen.getByText(/Cloud Services/i)).toBeInTheDocument();
    expect(screen.getByText(/Log Out/i)).toBeInTheDocument();
    expect(screen.getByText(/Refresh Page/i)).toBeInTheDocument();
    expect(screen.getByText(/Add Cloud/i)).toBeInTheDocument();
  });

  test('fetches cloud data and displays it', async () => {
    const mockClouds = [
      { cloud_name: 'Google Drive' },
      { cloud_name: 'Dropbox' },
    ];

    // Mock the axios response
    axios.get.mockResolvedValue({
      data: mockClouds,
    });

    // Mock the getAccessToken function
    getAccessToken.mockReturnValue('mockAccessToken');

    render(
      <MemoryRouter>
        <Main />
      </MemoryRouter>
    );

    // Wait for data to be fetched
    await waitFor(() => screen.getByText('Google Drive, Dropbox'));

    // Check if cloud services are rendered
    expect(screen.getByText('Google Drive, Dropbox')).toBeInTheDocument();
  });

  test('displays message when no cloud data is available', async () => {
    // Mock the axios response for empty data
    axios.get.mockResolvedValue({
      data: [],
    });

    // Mock the getAccessToken function
    getAccessToken.mockReturnValue('mockAccessToken');

    render(
      <MemoryRouter>
        <Main />
      </MemoryRouter>
    );

    // Wait for data to be fetched
    await waitFor(() => screen.getByText('No clouds available'));

    // Check if the fallback message is rendered
    expect(screen.getByText('No clouds available')).toBeInTheDocument();
  });

  test('clicking "Log Out" clears tokens and navigates to login', () => {
    const navigate = jest.fn();

    render(
      <MemoryRouter>
        <Main />
      </MemoryRouter>
    );

    // Mock navigate function
    const logoutButton = screen.getByText(/Log Out/i);
    fireEvent.click(logoutButton);

    // Check if localStorage is cleared
    expect(localStorage.getItem('accessToken')).toBeNull();
    expect(localStorage.getItem('refreshToken')).toBeNull();

    // Check if navigate function is called
    expect(navigate).toHaveBeenCalledWith('/login');
  });

  test('clicking "Refresh Page" reloads the page', () => {
    // Mock window.location.reload function
    const reloadMock = jest.fn();
    global.location.reload = reloadMock;

    render(
      <MemoryRouter>
        <Main />
      </MemoryRouter>
    );

    const refreshButton = screen.getByText(/Refresh Page/i);
    fireEvent.click(refreshButton);

    // Check if the page refresh function is called
    expect(reloadMock).toHaveBeenCalledTimes(1);
  });

  test('clicking "Add Cloud" navigates to add cloud page', () => {
    const navigate = jest.fn();

    render(
      <MemoryRouter>
        <Main />
      </MemoryRouter>
    );

    const addCloudButton = screen.getByText(/Add Cloud/i);
    fireEvent.click(addCloudButton);

    // Check if navigate function is called
    expect(navigate).toHaveBeenCalledWith('/addcloud');
  });

  test('TabsComponent renders with cloud data', async () => {
    const mockClouds = [
      { cloud_name: 'Google Drive' },
      { cloud_name: 'Dropbox' },
    ];

    // Mock the axios response
    axios.get.mockResolvedValue({
      data: mockClouds,
    });

    // Mock the getAccessToken function
    getAccessToken.mockReturnValue('mockAccessToken');

    render(
      <MemoryRouter>
        <Main />
      </MemoryRouter>
    );

    // Wait for data to be fetched and check if TabsComponent rendered with cloud data
    await waitFor(() => screen.getByText('Tabs rendered'));
    expect(screen.getByText('Tabs rendered')).toBeInTheDocument();
  });
});
