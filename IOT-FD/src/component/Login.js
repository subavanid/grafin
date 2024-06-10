import React, { useState } from "react";
import {
  TextField,
  Button,
  Typography,
  Container,
  Grid,
  InputAdornment,
  IconButton,
  Box,
} from "@mui/material";
import { Visibility, VisibilityOff } from "@mui/icons-material";
import Axios from "../config/Axios";
import { Link as RouterLink, useNavigate } from "react-router-dom";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [responseMessage, setResponseMessage] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (event) => {
    event.preventDefault();

    try {
      const response = await Axios.post("user/login/  ", {
        email: email,
        password: password,
      });

      console.log("Success ========>", response);
      if (response?.status === 200) {
        localStorage.setItem("token", response?.data?.Token);
        localStorage.setItem("userId", response?.data?.id);
        alert('User login successfully.');
        navigate("/dashboard"); 
      } else {
        setResponseMessage(
          "Invalid response from server. Please try again later."
        );
      }
    } catch (error) {
      console.error("Error ========>", error);
      if (error.response && error.response.status === 401) {
        // 401 Unauthorized - Invalid email or password
        setResponseMessage("Invalid email or password. Please try again.");
      } else if (error.request) {
        // Request made but no response received
        setResponseMessage("No response from server. Please try again later.");
      } else {
        // Other errors
        setResponseMessage("An error occurred. Please try again later.");
      }
    }
  };

  const handlePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  return (
    <Container
      sx={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "100vh",
        backgroundColor: "#30333C",
      }}
    >
      <Box
        component="form"
        onSubmit={handleLogin}
        sx={{
          width: "100%",
          maxWidth: "400px",
          backgroundColor: "white",
          p: 3,
          borderRadius: "8px",
          boxShadow: "0px 0px 20px 0px rgba(0,0,0,0.2)",
        }}
      >
        <Typography
          variant="h4"
          align="center"
          gutterBottom
          sx={{ color: "black" }}
        >
          Login
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <TextField
              label="Email"
              type="email"
              variant="outlined"
              fullWidth
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              type={showPassword ? "text" : "password"}
              label="Password"
              variant="outlined"
              fullWidth
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              InputProps={{
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      aria-label="toggle password visibility"
                      onClick={handlePasswordVisibility}
                      edge="end"
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />
          </Grid>
          <Grid item xs={12}>
            <Button
              sx={{ color: "black" }}
              type="submit"
              variant="contained"
              fullWidth
            >
              Login
            </Button>
            <Typography>{responseMessage}</Typography>
            <Typography>
              Don't have an account?{" "}
              <RouterLink to="/register">Register</RouterLink>
            </Typography>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default Login;
