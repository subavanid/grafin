import React, { useState } from 'react';
import { TextField, Button, Typography, Container, Grid, InputAdornment, IconButton, Box } from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import { Link as RouterLink } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import Axios from '../config/Axios';

const Register = () => {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
    });
    const navigate = useNavigate();

    const handleInputChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleRegister = async (event) => {
        event.preventDefault();
        try {
            await Axios.post("api/register", formData);
            alert('User registered successfully.');
            navigate('/');
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const [showPassword, setShowPassword] = useState(false);

    const handlePasswordVisibility = () => {
        setShowPassword(!showPassword);
    };

    return (
        <Container
            sx={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                minHeight: '100vh',
                backgroundColor: '#30333C',
            }}
        >
            <Box
                component="form"
                onSubmit={handleRegister}
                sx={{
                    width: '100%',
                    maxWidth: '400px',
                    backgroundColor: "#ffff",
                    p: 3,
                    borderRadius: '8px',
                    boxShadow: '0px 0px 20px 0px rgba(0,0,0,0.2)',
                }}
            >
                <Typography variant="h4" align="center" gutterBottom>
                    Register
                </Typography>
                <Grid container spacing={2}>
                    <Grid item xs={12}>
                        <TextField
                            label="Username"
                            type="text"
                            name="username"
                            variant="outlined"
                            fullWidth
                            value={formData.username}
                            onChange={handleInputChange}
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField
                            label="Email"
                            type="email"
                            name="email"
                            variant="outlined"
                            fullWidth
                            value={formData.email}
                            onChange={handleInputChange}
                        />
                    </Grid>
                    <Grid item xs={12}>
                        <TextField
                            type={showPassword ? 'text' : 'password'}
                            label="Password"
                            name="password"
                            variant="outlined"
                            fullWidth
                            value={formData.password}
                            onChange={handleInputChange}
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
                        <Button type="submit" variant="contained" color="primary" fullWidth>
                            Register
                        </Button>
                        <Typography>
                            Already have an account? <RouterLink to="/">Login</RouterLink>
                        </Typography>
                    </Grid>
                </Grid>
            </Box>
        </Container>
    );
};

export default Register;