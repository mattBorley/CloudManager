// AddCloud.test.js
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import AddCloud from "./AddCloud";  // Import the component
import axios from "axios";
import { BrowserRouter as Router } from "react-router-dom";  // To wrap the component in a Router for useNavigate
import { GoogleOAuthProvider } from "@react-oauth/google";  // To wrap the component in the OAuth provider

jest.mock("axios");  // Mocking axios

// Mocking navigate function
const mockNavigate = jest.fn();

beforeEach(() => {
  jest.clearAllMocks();  // Clear any mocks before each test
});

const setup = () => {
  return render(
    <GoogleOAuthProvider clientId="mock-client-id">
      <Router>
        <AddCloud />
      </Router>
    </GoogleOAuthProvider>
  );
};

describe("AddCloud Component", () => {
  test("renders correctly", () => {
    setup();

    expect(screen.getByText(/Add Cloud Service/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Enter the chosen name of this storage cloud/i)).toBeInTheDocument();
    expect(screen.getByText(/Select Cloud/i)).toBeInTheDocument();
  });

  test("displays error message when no cloud is selected", async () => {
    setup();

    fireEvent.click(screen.getByText(/Add cloud/i));

    expect(screen.getByText(/No service selected/i)).toBeInTheDocument();
  });

  test("displays error message when no cloud name is entered", async () => {
    setup();

    fireEvent.change(screen.getByPlaceholderText(/Enter the chosen name of this storage cloud/i), {
      target: { value: "" }
    });

    fireEvent.click(screen.getByText(/Add cloud/i));

    expect(screen.getByText(/❌ No service selected/i)).toBeInTheDocument();
  });

  test("triggers Google OAuth logic when Google Drive is selected", async () => {
    setup();

    fireEvent.change(screen.getByPlaceholderText(/Enter the chosen name of this storage cloud/i), {
      target: { value: "My Cloud" }
    });
    fireEvent.change(screen.getByLabelText(/Select Cloud/i), {
      target: { value: "google_drive" }
    });

    jest.mock('@react-oauth/google', () => {
      const googleLoginSpy = jest.fn();  // Moved inside
      return {
        useGoogleLogin: () => googleLoginSpy,
      };
    });
    fireEvent.click(screen.getByText(/Add cloud/i));

    expect(googleLoginSpy).toHaveBeenCalled();
  });

  test("initiates Box OAuth correctly", async () => {
    axios.get.mockResolvedValueOnce({ data: { auth_url: "https://box.com/auth" } });

    setup();

    fireEvent.change(screen.getByPlaceholderText(/Enter the chosen name of this storage cloud/i), {
      target: { value: "My Cloud" }
    });
    fireEvent.change(screen.getByLabelText(/Select Cloud/i), {
      target: { value: "box" }
    });

    fireEvent.click(screen.getByText(/Add cloud/i));

    await waitFor(() => {
      expect(axios.get).toHaveBeenCalledWith("http://localhost:5000/api/box/authorization", { withCredentials: true });
      expect(window.location.href).toBe("https://box.com/auth");
    });
  });

  test("initiates Dropbox OAuth correctly", async () => {
    axios.get.mockResolvedValueOnce({ data: { auth_url: "https://dropbox.com/auth" } });

    setup();

    fireEvent.change(screen.getByPlaceholderText(/Enter the chosen name of this storage cloud/i), {
      target: { value: "My Cloud" }
    });
    fireEvent.change(screen.getByLabelText(/Select Cloud/i), {
      target: { value: "dropbox" }
    });

    fireEvent.click(screen.getByText(/Add cloud/i));

    await waitFor(() => {
      expect(axios.get).toHaveBeenCalledWith("http://localhost:5000/api/dropbox/authorization", { withCredentials: true });
      expect(window.location.href).toBe("https://dropbox.com/auth");
    });
  });

  test("navigates back to main on clicking back button", () => {
    setup();

    fireEvent.click(screen.getByText(/Back/i));

    expect(mockNavigate).toHaveBeenCalledWith("/main");
  });
});
