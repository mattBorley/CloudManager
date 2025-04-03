import axios from "axios";
import { useEffect } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { Card } from "@chakra-ui/react";
import "../styling/apiLoading.css";

const DropboxCallback = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  useEffect(() => {
    const handleCallback = async () => {
      console.log("Handling OAuth callback...");
      const code = searchParams.get("code");
      const state = searchParams.get("state");
      const cloudName = localStorage.getItem("cloudName");
      localStorage.removeItem("cloudName");

      console.log("Extracted code:", code);
      console.log("Extracted state:", state);
      console.log("Extracted cloudName:", cloudName);

      if (!code) {
        console.error("No authorization code found.");
        navigate("/addcloud");
        return;
      }

      if (!state) {
        console.error("No state found.");
        navigate("/addcloud");
        return;
      }

      if (!cloudName) {
        console.error("No cloud name found.");
        navigate("/addcloud");
        return;
      }

      const accessToken = localStorage.getItem("accessToken");
      console.log("Using accessToken:", accessToken);

      try {
        console.log("Sending request to backend...");
        await axios.get("http://localhost:8000/api/dropbox/callback", {
          params: { code, state, cloud_name: cloudName },
          headers: { Authorization: `Bearer ${accessToken}` },
          withCredentials: true,
        });

        console.log("OAuth callback handled successfully, navigating to /main");
        navigate("/main");
      } catch (error) {
        console.error("Error handling Dropbox OAuth callback:", error);
        navigate("/addcloud");
      }
    };

    handleCallback();
  }, [searchParams, navigate]);


  return (
    <Card
      bg={"#4e4e4e"}
      position={"absolute"}
      minH={"100%"}
      w={"100%"}
      p={4}
      display="flex"
      alignItems={"center"}
      flexDir={"column"}
      borderRadius={"0"}
    >
      <h2 className={"title"}>Processing Dropbox OAuth Callback...</h2>
    </Card>
  );
};

export default DropboxCallback;
