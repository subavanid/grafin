import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { styled, useTheme, alpha } from '@mui/material/styles';
import Box from '@mui/material/Box';
import CssBaseline from '@mui/material/CssBaseline';
import MuiAppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import Sidebar from '../component/Sidebar';
import InputBase from '@mui/material/InputBase';
import SearchIcon from '@mui/icons-material/Search';
import DomainIcon from '@mui/icons-material/Domain';
import CloudIcon from '@mui/icons-material/Cloud';
import { BarChart, LineChart } from '@mui/x-charts';

import { Grid, Button, Card, CardActions, CardContent } from '@mui/material';
import "../App.css";


const drawerWidth = 240;

const Main = styled('main', { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    flexGrow: 1,
    padding: theme.spacing(3),
    transition: theme.transitions.create('margin', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    marginLeft: -`${drawerWidth}px`,
    ...(open && {
      transition: theme.transitions.create('margin', {
        easing: theme.transitions.easing.easeOut,
        duration: theme.transitions.duration.enteringScreen,
      }),
      marginLeft: 0,
    }),
  }),
);

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }) => ({
  transition: theme.transitions.create(['margin', 'width'], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    width: `calc(100% - ${drawerWidth}px)`,
    marginLeft: `${drawerWidth}px`,
    transition: theme.transitions.create(['margin', 'width'], {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
      backgroundColor: "black",
    }),
  }),
}));

const DrawerHeader = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  padding: theme.spacing(0, 1),
  ...theme.mixins.toolbar,
  justifyContent: 'flex-end',
}));

const Search = styled('div')(({ theme }) => ({
  position: 'relative',
  borderRadius: theme.shape.borderRadius,
  borderColor: '#387e8a',
  backgroundColor: alpha(theme.palette.common.white, 0.15),
  '&:hover': {
    backgroundColor: alpha(theme.palette.common.white, 0.25),
  },
  marginLeft: 0,
  width: 'auto',
  [theme.breakpoints.up('sm')]: {
    marginLeft: theme.spacing(1),
    width: 'auto',
  },
}));

const SearchIconWrapper = styled('div')(({ theme }) => ({
  padding: theme.spacing(0, 2),
  height: '100%',
  position: 'absolute',
  pointerEvents: 'none',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
  color: 'inherit',
  width: '100%',
  '& .MuiInputBase-input': {
    padding: theme.spacing(1, 1, 1, 0),
    paddingLeft: `calc(1em + ${theme.spacing(4)})`,
    transition: theme.transitions.create('width'),
    [theme.breakpoints.up('sm')]: {
      width: '12ch',
      '&:focus': {
        width: '20ch',
      },
    },
  },
}));

const Dashboard = ({ username }) => {
  const theme = useTheme();
  const [open, setOpen] = React.useState(true);

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  return (
    <Box sx={{ display: 'flex', backgroundColor: "#021816", height: "100vh" }}>
      <CssBaseline />
      <AppBar position="fixed" open={open} sx={{ backgroundColor: "#30333c" }}>
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            onClick={handleDrawerOpen}
            edge="start"
            sx={{ mr: 2, ...(open && { display: 'none' }) }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div">
            Dashboard {username}
          </Typography>
        </Toolbar>
      </AppBar>
      <Sidebar open={open} onClose={handleDrawerClose} />
      <Main open={open} sx={{width:"100vw"}}>
        <DrawerHeader />
        <Grid container spacing={2} sx={{ maxHeight: "100vh",display: 'flex', justifyContent: 'space-between', mt: 4 }}>
        <Grid item xs={12} sx={{ display: 'flex', justifyContent: 'space-between', mt: 2 }}>
          <Grid item xs={6} sx={{display:"flex",justifyContent:"flex-start"}}>
            <Search sx={{backgroundColor:"white"}}>
              <SearchIconWrapper>
                <SearchIcon />
              </SearchIconWrapper>
              <StyledInputBase sx={{ border: "blue" }}
                placeholder="Search…"
                inputProps={{ 'aria-label': 'search' }}
              />
            </Search>
            </Grid>
            <Grid item xs={6} sx={{display:"flex",justifyContent:"flex-end"}}>
            <Link to="/" style={{ textDecoration: 'none' }}>
              <Button variant="contained" href="#contained-buttons" sx={{ borderRadius: 70, backgroundColor: '#387e8a', ml: 1 }}>
                Logout
              </Button>
            </Link>
          </Grid>
          </Grid>
          <Grid item container xs={12} spacing={2} sx={{ maxHeight: "100%",display: 'flex', justifyContent: 'space-between', mt: 4 }}>
            <Grid item xs={12} sm={6} md={4} sx={{display:"flex",justifyContent:"flex-start"}}>
              <Card sx={{ minWidth: 250, display: 'flex', flexDirection: 'column', justifyContent: 'space-between',height: 130,width:400 }}>
                <Box sx={{ height: 130, display: 'flex', justifyContent: 'space-between', background: "linear-gradient(transparent, #387e8a 75%), linear-gradient(transparent, white 75%)" }}>
                  <CardContent>
                    <Typography variant="h5" component="div">
                      Total Places
                    </Typography>
                    <Typography variant="h5" component="div">
                       2
                    </Typography>
                  </CardContent>
                  <CardActions>
                    <DomainIcon sx={{marginRight:"30px"}} />
                  </CardActions>
                </Box>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={4} sx={{display:"flex",justifyContent:"flex-end"}}>
              <Card sx={{ minWidth: 250, display: 'flex', flexDirection: 'column', justifyContent: 'space-between',height: 130,width:400 }}>
                <Box sx={{ height: 130, display: 'flex', justifyContent: 'space-between', background: "linear-gradient(transparent, #387e8a 75%), linear-gradient(transparent, white 75%)" }}>
                  <CardContent>
                    <Typography variant="h5" component="div">
                      Weather Today
                    </Typography>
                    <Typography variant="h5" component="div">
                      25°C
                    </Typography>
                  </CardContent>
                  <CardActions>
                    <CloudIcon sx={{marginRight:"30px"}} />
                  </CardActions>
                </Box>
              </Card>
            </Grid>
          </Grid>
        </Grid>
      </Main>
    </Box>
  );
}

export default Dashboard;
