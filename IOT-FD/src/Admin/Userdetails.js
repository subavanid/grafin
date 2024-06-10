// import React, { useEffect, useState } from 'react';
// import { Typography, Card, CardContent, Grid } from '@mui/material';
// import Axios from "../config/Axios";
// import { useParams } from 'react-router-dom';

// export default function UserDetails() {
//   const { id } = useParams();
//   const [user, setUserDetails] = useState(null);

//   useEffect(() => {
//     const fetchUserDetails = async () => {
//       try {
//         const token = localStorage.getItem("token");

//         const response = await Axios.get(`adminpanel/api/userdetails/${id}`, {
//           headers: {
//             'Authorization': `Token ${token}`,
//           }
//         });
//         setUserDetails(response.data);
//       } catch (error) {
//         console.error('Error fetching user details:', error);
//       }
//     };

//     fetchUserDetails();
//   }, [id]);

//   if (!user) return <div>Loading...</div>;

//   return (
//     <Grid container padding="10px">
//       <Grid item xs={12}>
//         <Card sx={{ minWidth: 275, minHeight: 100, backgroundColor: '#387e8a', margin: 1 }}>
//           <CardContent>
//             <Typography variant="body2" color="white">
//               <strong>Full User Details:</strong><br />
//               ID: {user.id}<br />
//               Username: {user.username}<br />
//               Email: {user.email}<br /> 
//               {user.home_appliances && (
//                 <>
//                   <Typography variant="body2" color="white">
//                     <strong>Home Appliances:</strong><br />
//                     {user.home_appliances.map((appliance, idx) => (
//                       <div key={idx}>
//                         Appliance ID: {user.appliancenamd}<br />
//                         Appliance Type: {appliance.type}<br />
//                       </div>
//                     ))}
//                   </Typography>
//                 </>
//               )}
//             </Typography>
//           </CardContent>
//         </Card>
//       </Grid>
//     </Grid>
//   );
// }
