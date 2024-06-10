import React, { useEffect, useState } from 'react';
import { Typography, Card, CardContent, Grid, Button } from '@mui/material';  // Make sure to import Button
import Axios from "../config/Axios";

export default function User() {
  const [details, setDetails] = useState([]);
  const [total, setTotal] = useState(0);
  const [selectedUser, setSelectedUser] = useState(null);
  const [user, setUserDetails] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem("token");
        
        const response = await Axios.get('api/users/details/', {
          headers: {
            'Authorization': `Token ${token}`,
          }
        });
        setTotal(response.data.total_count);
        setDetails(response.data.users);
      } catch (error) {
        console.error('Error fetching data:', error);

        if (error.response) {
          console.error('Error response data:', error.response.data);
          console.error('Error response status:', error.response.status);
          console.error('Error response headers:', error.response.headers);
        } else if (error.request) {
          console.error('Error request:', error.request);
        } else {
          console.error('Error message:', error.message);
        }
      }
    };

    fetchData();
  }, []);

  const fetchUserDetails = async (userId) => {
    try {
      const token = localStorage.getItem("token");

      const response = await Axios.get(`adminpanel/api/userdetails/${userId}`, {
        headers: {
          'Authorization': `Token ${token}`,
        }
      });
      setUserDetails(response.data);
    } catch (error) {
      console.error('Error fetching user details:', error);

      if (error.response) {
        console.error('Error response data:', error.response.data);
        console.error('Error response status:', error.response.status);
        console.error('Error response headers:', error.response.headers);
      } else if (error.request) {
        console.error('Error request:', error.request);
      } else {
        console.error('Error message:', error.message);
      }
    }
  };

  useEffect(() => {
    if (selectedUser) {
      fetchUserDetails(selectedUser);
    }
  }, [selectedUser]);

  return (
    <Grid container padding="10px">
      <Grid item xs={12}>
        <Card sx={{ minWidth: 275, minHeight: 100, backgroundColor: '#387e8a', margin: 1 }}>
          <CardContent>
            <Typography variant="body2" color="white">
              Total Users: {total}
            </Typography>
          </CardContent>
        </Card>
      </Grid>
      {details.map((user, index) => (
        <Grid item xs={6} key={index}>
          <Card sx={{ minWidth: 275, minHeight: 100, backgroundColor: '#387e8a', margin: 1 }}>
            <CardContent>
              <Typography variant="body2" color="white">
                Username: {user.username}<br />
                Email: {user.email}<br />
              </Typography>
              <Button 
                variant="contained" 
                color="primary" 
                onClick={() => setSelectedUser(user.id)}
              >
                View Details    
              </Button>
            </CardContent>
          </Card>
        </Grid>
      ))}
      {user && (
        <Grid item xs={12}>
          <Card sx={{ minWidth: 275, minHeight: 100, backgroundColor: '#387e8a', margin: 1 }}>
            <CardContent>
                    <Typography variant="body2" color="white">
                      <strong>Home Appliances:</strong><br />
                      {user.map((appliance, idx) => (
                        <div key={idx}> 
                          Appliance ID: {appliance.appliancename}<br />
                          Appliance Type: {appliance.switchname}<br />
                        </div>
                      ))}
                    </Typography>
            </CardContent>
          </Card>
        </Grid>
      )}
    </Grid>
  );
}
