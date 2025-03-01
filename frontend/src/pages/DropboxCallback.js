import axios from "axios";
import { useEffect } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import {Card} from "@chakra-ui/react";
import "../styling/apiLoading.css"

const DropboxCallback = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  useEffect(() => {
    const handleCallback = async () => {
      const code = searchParams.get("code");

      if (!code) {
        console.error("No authorization code found.");
        navigate("/addcloud");
        return;
      }

      try {
        const response = await axios.get("http://localhost:8000/api/dropbox/callback", {
          params: { code },
          withCredentials: true,
        });

        console.log("Dropbox OAuth Success:", response.data);

        navigate("/main");
      } catch (error) {
        console.error("Error handling Dropbox OAuth callback:", error);
        navigate("/addcloud");
      }
    };

    handleCallback();
  }, []);

  return (
      <Card
            bg={"#4e4e4e"}
            position={"absolute"}
            minH={"100%"}
            w={"100%"}
            p={4}
            display = "flex"
            alignItems={"center"}
            flexDir={"column"}
            borderRadius={"0"}
        >
          <h2 className={"title"}>Processing Dropbox OAuth Callback...</h2>

      </Card>
  );
};

export default DropboxCallback;
