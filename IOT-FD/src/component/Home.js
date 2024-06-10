import * as React from 'react';
import { useState, useEffect } from 'react';
import { styled, useTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import CssBaseline from '@mui/material/CssBaseline';
import MuiAppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import { alpha } from '@mui/material/styles';
import InputBase from '@mui/material/InputBase';
import SearchIcon from '@mui/icons-material/Search';
import { Grid, Button, Card, CardContent } from '@mui/material';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Modal from 'react-modal';
import CloseIcon from '@mui/icons-material/Close';
import Cookies from 'js-cookie';
import Axios from "../config/Axios";
import "../App.css";
import Sidebar from './Sidebar';
import EditIcon from '@mui/icons-material/Edit';
import VisibilityIcon from '@mui/icons-material/Visibility';
import DeleteIcon from '@mui/icons-material/Delete';
import { useNavigate, useParams,useSearchParams } from 'react-router-dom'; // Import only necessary hooks

const customStyles = {
  content: {
    top: '50%',
    left: '50%',
    right: 'auto',
    bottom: 'auto',
    marginRight: '-50%',
    transform: 'translate(-50%, -50%)',
  },
};

let userId = Cookies.get('userId');

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

const Home = ({ username }) => {
  // const history = useHistory();
  const { roomId } = useParams(); // Import only necessary hooks

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

  const [userId, setUserId] = useState(null);
  const navigate = useNavigate();
  const theme = useTheme();
  const [open, setOpen] = React.useState(true);
  const [newRoomName, setNewRoomName] = useState('');
  const [rooms, setRooms] = useState([]);
  const [ismodalIsOpen, setIsModalOpen] = useState(false);
  const [selectedRoom, setSelectedRoom] = useState('');
  const [updateModalIsOpen, setUpdateModalIsOpen] = useState(null);
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [queryParameters] = useSearchParams();

  useEffect(() => {
    const storedUserId = localStorage.getItem('userId');
    if (storedUserId) {
      setUserId(storedUserId);
      fetchRooms(storedUserId);
    } else {
      toast.error('User ID not found. Please log in.');
    }
  }, []);

  const openModal = () => {
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setNewRoomName('');
  };

  const openUpdateModal = (item) => {
    setSelectedRoom({id: item.room_id});
    setUpdateModalIsOpen(true);
  };

  const closeUpdateModal = () => {
    setUpdateModalIsOpen(false);
    setSelectedRoom('');
  };

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  const fetchRooms = async (userId) => {
    try {
      const token = localStorage.getItem('token');
      const user_id = localStorage.getItem('userId');
      console.log("user_id", user_id);
      const response = await Axios.get('home/get_room/'+ user_id, {
        headers: {
          'Authorization': `Token ${token}`,
        }
      });
      if (response.status === 200) {
        setRooms(response.data.room_details);
        console.log(response.data)
      } else {
        toast.error('Failed to fetch rooms');
      }
    } catch (error) {
      toast.error('Error fetching rooms: ' + error.message);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!newRoomName) {
      toast.error('Please enter a room name');
      return;
    }
    try {
      const token = localStorage.getItem('token');
      const addedBy = localStorage.getItem("id");
      const response = await Axios.post(
        '/home/add_room/',
        { room: newRoomName, added_by: addedBy },
        {
          headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (response.status === 201) {
        toast.success('Room added successfully!');
        fetchRooms(userId);
        closeModal();
      } else {
        toast.error('Error adding room');
      }
    } catch (error) {
      console.error('Error adding room:', error);
      toast.error('Error adding room: ' + error.message);
    }
  };

  const handleDeleteRoom = async (roomId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await Axios.delete(`/api/homeroom/deletehomeroom/${roomId}`, {
        headers: {
          'Authorization': `Token ${token}`,
        }
      });
      if (response.status === 204) {
        // If deletion is successful, fetch updated rooms
        fetchRooms();
        toast.success('Room deleted successfully!');
      } else {
        toast.error('Failed to delete room');
      }
    } catch (error) {
      toast.error('Error deleting room: ' + error.message);
    }
  };

  // const handleUpdateRoom = async (roomId) => {
  //   try {
  //     const token = localStorage.getItem('token');
  //     const response = await Axios.put(`/api/homeroom/update_home_room/${roomId}`, {
  //       headers: {
  //         'Authorization': `Token ${token}`,
  //       }
  //     });
  //     if (response.status === 204) {
  //       // If deletion is successful, fetch updated rooms
  //       fetchRooms();
  //       toast.success('Room Updated successfully!');
  //     } else {
  //       toast.error('Failed to Update room');
  //     }
  //   } catch (error) {
  //     toast.error('Error Updating room: ' + error.message);
  //   }
  // };
  const handleUpdateSubmit = async (event) => {
    event.preventDefault();
    if (!selectedRoom?.room_name) {
      toast.error('Please enter a room name');
      return;
    }
    try {
      const token = localStorage.getItem('token');
      console.log(selectedRoom.id,"8976543");
      const response = await Axios.put(
        `/api/homeroom/update_home_room/${selectedRoom.id}`,
        { room: selectedRoom.room_name, added_by: selectedRoom.added_by },
        {
          headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (response.status === 200) {
        toast.success('Room updated successfully!');
        fetchRooms(userId);
        closeUpdateModal();
      } else {
        toast.error('Error updating room');
      }
    } catch (error) {
      console.error('Error updating room:', error);
      toast.error('Error updating room: ' + error.message);
    }
  };

  // const navigateToRoom = (roomId) => {
  //   navigate(`/room/${roomId}`);
  //   console.log(roomId,"***********");
  // };

  return (
    <Box sx={{ display: 'flex', height: "auto", backgroundColor: "black" }}>
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
            Home {username}
          </Typography>
        </Toolbar>
      </AppBar>
      <Sidebar open={open} onClose={handleDrawerClose} /> {/* Replace Drawer with Sidebar */}
      <Main open={open}>
        <DrawerHeader />
        <Grid container spacing={2} sx={{ maxHeight: "100%" }}>
          <Grid item xs={12} sx={{ display: 'flex', justifyContent: 'space-between', mt: 2 }}>
          <Grid item xs={6} sx={{display:"flex",justifyContent:"flex-start"}}>
            <Search sx={{backgroundColor:"white"}}>
              <SearchIconWrapper>
                <SearchIcon />
              </SearchIconWrapper>
              <StyledInputBase
                placeholder="Search…"
                inputProps={{ 'aria-label': 'search' }}
              />
            </Search>
            </Grid>
            <Grid item xs={6} sx={{display:"flex",justifyContent:"flex-end"}}>
            <Button variant="contained" onClick={openModal} sx={{ borderRadius: 70, backgroundColor: '#387e8a', ml: 1}}>
              AddRoom
            </Button>
            </Grid>
          </Grid>
          <Modal
              isOpen={ismodalIsOpen}
              onRequestClose={closeModal}
              style={customStyles}
              contentLabel="Add Room Modal"
            >
              <div>
                <CloseIcon onClick={closeModal} style={{ position: 'absolute', top: 10, right: 10, cursor: 'pointer' }} />
                <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                  <input
                    type="text"
                    placeholder="Enter Room Name"
                    value={newRoomName}
                    onChange={(event) => setNewRoomName(event.target.value)}
                    style={{
                      width: '80%',
                      padding: '10px',
                      marginTop: '20px',
                      borderRadius: '5px',
                      border: '1px solid #ccc',
                      fontSize: '16px',
                    }}
                  />
                  <br></br><br></br>
                  <button type="submit" style={{
                    backgroundColor: '#387e8a',
                    color: 'white',
                    padding: '10px 20px',
                    marginTop: '20px',
                    borderRadius: '5px',
                    border: 'none',
                    fontSize: '16px',
                  }}>Submit</button>
                </form>
              </div>
          </Modal>
          <Modal
          isOpen={updateModalIsOpen}
          onRequestClose={closeUpdateModal}
          style={customStyles}
          contentLabel="Update Room Modal"
        >
          <h2>Update Room</h2>
          <form onSubmit={handleUpdateSubmit}>
            <input
              type="text"
              placeholder="Enter room name"
              value={selectedRoom?.room_name || ''}
              onChange={(e) => setSelectedRoom({ ...selectedRoom, room_name: e.target.value })}
            />
            <Button variant="contained" color="primary" type="submit">
              Update Room
            </Button>
            <Button variant="contained" color="secondary" onClick={closeUpdateModal}>
              Cancel
            </Button>
          </form>
        </Modal>
          {/* <Grid container spacing={2}> */}
            <Grid item container xs={12} spacing={2} justifyContent="center">
              {rooms.map((item,index)=> ( 
                <Grid key={item.room_id} item xs={12} sm={6} md={4}>
            {/* <Grid onClick={() => navigateToRoom(item.room_id)}></Grid> */}
                  <Card sx={{ minWidth: 250, display: 'flex', flexDirection: 'column', justifyContent: 'space-between', cursor: 'pointer',background: "linear-gradient(transparent, #387e8a 100%), linear-gradient(transparent, white 100%)",border:"1px solid #fff"}}>
                    <CardContent>
                        <Typography variant="h5" component="div" sx={{color:"white"}}>
                          {item.room_name}
                        </Typography>
                        <Box sx={{display:"flex",justifyContent:"flex-end"}}>
                        <VisibilityIcon onClick={() => {
                  // navigateToRoom(item.room_id)  
                  const roomType = item.room_name ? item.room_name : 'unknown';
                  // console.log("#####", item.room_id)
                  navigate(`/rooms?place=home&roomtype=${roomType}&roomId=${item.room_id}`);
                          
                }} sx={{color:"black"}} />    
                        {/* <EditIcon sx={{color:"black"}} onClick={() => openUpdateModal(item)} />
                        <DeleteIcon onClick={() => handleDeleteRoom(item.room_id)} sx={{color:"black"}} />  */}
                        </Box>                     
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          {/* </Grid> */}
        </Grid>
      </Main>
    </Box>
  );
}

export default Home;
