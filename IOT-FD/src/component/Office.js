import * as React from 'react';
import { useState, useEffect } from 'react';
import { styled, useTheme, alpha } from '@mui/material/styles';
import {
  Box,
  Drawer,
  CssBaseline,
  AppBar as MuiAppBar,
  Toolbar,
  Typography,
  IconButton,
  InputBase,
  Grid,
  Button,
  Card,
  CardContent,
} from '@mui/material';
import { Search as SearchIcon, Menu as MenuIcon, Close as CloseIcon, Edit as EditIcon, Visibility as VisibilityIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Modal from 'react-modal';
import Axios from "../config/Axios";
import "../App.css";
import Sidebar from './Sidebar';
import Cookies from 'js-cookie';
import { useNavigate, useParams, useSearchParams } from 'react-router-dom';

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
    marginLeft: -drawerWidth,
    ...(open && {
      transition: theme.transitions.create('margin', {
        easing: theme.transitions.easing.easeOut,
        duration: theme.transitions.duration.enteringScreen,
      }),
      marginLeft: 0,
    }),
  }),
);

const Office = ({ username }) => {
  const { roomId } = useParams();
  const AppBar = styled(MuiAppBar, { shouldForwardProp: (prop) => prop !== 'open' })(
    ({ theme, open }) => ({
      transition: theme.transitions.create(['margin', 'width'], {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
      }),
      ...(open && {
        width: `calc(100% - ${drawerWidth}px)`,
        marginLeft: drawerWidth,
        transition: theme.transitions.create(['margin', 'width'], {
          easing: theme.transitions.easing.easeOut,
          duration: theme.transitions.duration.enteringScreen,
        }),
      }),
    })
  );

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

  const [open, setOpen] = useState(true);
  const navigate = useNavigate();
  const [newRoomName, setNewRoomName] = useState('');
  const [officerooms, setRooms] = useState([]);
  const [ismodalIsOpen, setIsModalOpen] = useState(false);
  const [selectedRoom, setSelectedRoom] = useState('');
  const [updateModalIsOpen, setUpdateModalIsOpen] = useState(false);
  const [queryParameters] = useSearchParams();

  useEffect(() => {
    const storedUserId = localStorage.getItem('userId');
    if (storedUserId) {
      userId = storedUserId;
      fetchRooms();
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
    setSelectedRoom({ id: item.room_id, room_name: item.office_room_name, added_by: item.added_by });
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

  const fetchRooms = async () => {
    try {
      console.log("fetch room");
      const token = localStorage.getItem('token');
      const response = await Axios.get(`office/get_room/${userId}`, {
        headers: {
          'Authorization': `Token ${token}`,
        },
      });
      if (response.status === 200) {
        setRooms(response.data.room_details);
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
        'office/add_room/',
        { officeroom: newRoomName, added_by: addedBy },
        {
          headers: {
            'Authorization': `Token ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (response.status === 201) {
        fetchRooms();
        toast.success('Room added successfully!');
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
      const response = await Axios.delete(`/api/officeroom/deleteofficeroom/${roomId}`, {
        headers: {
          'Authorization': `Token ${token}`,
        }
      });
      if (response.status === 204) {
        fetchRooms();
        toast.success('Room deleted successfully!');
      } else {
        toast.error('Failed to delete room');
      }
    } catch (error) {
      toast.error('Error deleting room: ' + error.message);
    }
  };

  

  const handleUpdateSubmit = async (event) => {
    event.preventDefault();
    if (!selectedRoom?.room_name) {
      toast.error('Please enter a room name');
      return;
    }
    try {
      const token = localStorage.getItem('token');
      const response = await Axios.put(
        `/api/officeroom/update_office/${selectedRoom.id}`,
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
        fetchRooms();
        closeUpdateModal();
      } else {
        toast.error('Error updating room');
      }
    } catch (error) {
      console.error('Error updating room:', error);
      toast.error('Error updating room: ' + error.message);
    }
  };

  return (
    <Box sx={{ display: 'flex', height: "120vh", backgroundColor: "black" }}>
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
            Office {username}
          </Typography>
        </Toolbar>
      </AppBar>
      <Sidebar open={open} onClose={handleDrawerClose} />
      <Main open={open}>
        <DrawerHeader />
        <Grid container spacing={2} sx={{ maxHeight: "100%" }}>
          <Grid item xs={12} sx={{ display: 'flex', justifyContent: 'space-between', mt: 2 }}>
            <Grid item xs={6} sx={{ display: "flex", justifyContent: "flex-start" }}>
              <Search sx={{ backgroundColor: "white" }}>
                <SearchIconWrapper>
                  <SearchIcon />
                </SearchIconWrapper>
                <StyledInputBase
                  placeholder="Search…"
                  inputProps={{ 'aria-label': 'search' }}
                />
              </Search>
            </Grid>
            <Grid item xs={6} sx={{ display: "flex", justifyContent: "flex-end" }}>
              <Button variant="contained" onClick={openModal} sx={{ borderRadius: 70, backgroundColor: '#387e8a', ml: 1 }}>
                Add Room
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
                <br />
                <br />
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
          <Grid item container xs={12} spacing={2} justifyContent="center">
            {officerooms.map((item) => (
              <Grid key={item.room_id} item xs={12} sm={6} md={4}>
                <Card sx={{
                  minWidth: 250,
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'space-between',
                  cursor: 'pointer',
                  background: "linear-gradient(transparent, #387e8a 100%), linear-gradient(transparent, white 100%)",
                  border: "1px solid #fff"
                }}>
                  <CardContent>
                    <Typography variant="h5" component="div" sx={{ color: "white" }}>
                      {item.office_room_name}
                    </Typography>
                    <Box sx={{ display: "flex", justifyContent: "flex-end" }}>
                      <VisibilityIcon onClick={() => {
                        const roomType = item.office_room_name ? item.office_room_name : 'unknown';
                        navigate(`/rooms?place=office&roomtype=${roomType}&roomId=${item.room_id}`);
                      }} sx={{ color: "black" }} />
                      {/* <EditIcon sx={{ color: "black" }} onClick={() => openUpdateModal(item)} />
                      <DeleteIcon onClick={() => handleDeleteRoom(item.room_id)} sx={{ color: "black" }} /> */}
                    </Box>  
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Grid>
      </Main>
    </Box>
  );
};

export default Office;
