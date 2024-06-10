import React, { useState, useEffect } from 'react';
import { Grid, Button, Typography, Card, Modal, TextField, Box, CardContent,Switch } from '@mui/material';
import Axios from "../config/Axios";
import CloseIcon from '@mui/icons-material/Close';
import { useParams, useSearchParams } from 'react-router-dom';
import EditIcon from '@mui/icons-material/Edit';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import DeleteIcon from '@mui/icons-material/Delete';
import '../App.css';



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

const AddApplianceModal = ({ isOpen, onClose, onSave }) => {
  const [addApplianceModal, setAddApplianceModal] = useState({
    "name": "",
    "room": "",
    "switch": ""
  })
  

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await onSave(addApplianceModal);
      onClose();
    } catch (error) {
      console.error('Error adding appliance:', error);
    }
  };

  return (
    <Modal sx={{ backgroundColor: "#4d4737", height: "50%" }}
      open={isOpen}
      onRequestClose={onClose}
      style={customStyles}
      contentLabel="Add Appliance Modal"
    >
      <div>
        <CloseIcon onClick={onClose} style={{ position: 'absolute', top: 10, right: 10, cursor: 'pointer', color: "white" }} />
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <input
            type="text"
            placeholder="Switch Name"
            value={addApplianceModal?.switch}
            onChange={(e) => { setAddApplianceModal((prev) => ({ ...prev, "switch": e.target.value })) }}
            style={{
              width: '80%',
              padding: '10px',
              marginTop: '20px',
              borderRadius: '5px',
              border: '1px solid #ccc',
              fontSize: '16px',
            }}
          />
          <input
            type="text"
            placeholder="Appliances Name"
            value={addApplianceModal?.name}
            onChange={(e) => { setAddApplianceModal((prev) => ({ ...prev, "name": e.target.value })) }}
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
          }}  >Submit</button>
        </form>
      </div>
    </Modal>
  );
};


const Room = () => {
  const [appliances, setAppliances] = useState([]);
  const [officeappliances, setOfficeAppliances] = useState([]);
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [editModel, setEditModel] = useState({
    "id": "",
    "name": "",
    "switch": ""
  });
  const [queryParameters] = useSearchParams();
  const token = localStorage.getItem("token");
  const [isEditOpen, setIsEditOpen] = useState(false);

  const fetchHomeAppliances = async (room_id) => {
    try {
      const token = localStorage.getItem('token');
      const response = await Axios.get(`appliances/room/${room_id}`, {
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        }
      });console.log(response.data.data);
      setAppliances(response.data.data);
    } catch (error) {
      console.error('Error fetching appliances:', error);
    }
  };

  const fetchOfficeAppliances = async (room_id) => {
    try {
          const token =localStorage.getItem("token")
      const response = await Axios.get(`appliances/office_room/${room_id}`,{
        headers: {
          'Authorization': `Token ${token}`,  
          'Content-Type': 'application/json'
        }
      });
      console.log(response.data.appliance_data);
      setOfficeAppliances(response.data.office_details.appliances);
    } catch (error) {
      console.error('Error fetching appliances:', error);
    }
  };

  useEffect(() => {
    if (queryParameters.get("place") === "home") {
      const room_id = queryParameters.get("roomId");
      if (room_id) {
        fetchHomeAppliances(room_id);
      }
    } else if(queryParameters.get("place") === "office") {
      console.log("office");
      const room_id = queryParameters.get("roomId");
      fetchOfficeAppliances(room_id);
    }
  }, [queryParameters]);

  // const handleSubmit = async (addApplianceModal) => {
  //   try {
  //     const roomID = queryParameters.get("roomId")
  //     const response = await Axios.post(`/api/add_officeappliances/${roomID}`, { name: addApplianceModal?.name, switchname: addApplianceModal?.switch }, {
  //       headers: {
  //         'Authorization': `Token ${token}`,
  //         'Content-Type': 'application/json'
  //       }
  //     });
  //     fetchHomeAppliances(roomID);
  //   } catch (error) {
  //     console.error('Error adding appliance:', error);
  //   }
  // };

    const handleHomeApplianceDelete = async (appliance) => {
    try {
      const token = localStorage.getItem('token');
      const response = await Axios.delete(`home/delete_appliance/${appliance.id}`, {
        headers: {
          'Authorization': `Token ${token}`,
        }
      });
      if (response.status === 204) {
        // If deletion is successful, fetch updated rooms
        fetchHomeAppliances(appliance.room_id);
        toast.success('Room deleted successfully!');
      } else {
        toast.error('Failed to delete room');
      }
    } catch (error) {
      toast.error('Error deleting room: ' + error.message);
    }
  };
  const handleSubmit = async (addApplianceModal) => {
    try {
      const roomID = queryParameters.get("roomId");
      const place = queryParameters.get("place");
      let url = ''; 
  
      if (place === 'home') {
        url = `home/add_appliance/${roomID}`;
      } else if (place === 'office') {
        url = `office/add_appliance/${roomID}`;
      } else {
        console.error('Invalid place:', place);
        return;
      }
  
      const response = await Axios.post(url, { name: addApplianceModal?.name, switchname: addApplianceModal?.switch }, {
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        }
      });
  
      // Fetch appliances based on place after adding the new appliance
      place === 'home' ? fetchHomeAppliances(roomID) : fetchOfficeAppliances(roomID);
    } catch (error) {
      console.error('Error adding appliance:', error);
    }
  };
  

  const handleEditSubmit = async (e) => {
    e.preventDefault();
    try {
      console.log("id----"+editModel.id)
      const roomID = queryParameters.get('roomId')
      console.log("roomId----"+roomID)
      let url=queryParameters.get("place")=="home"?`home/update_appliance/${editModel.id}`:`office/update_appliance/${editModel.id}`
      const response = await Axios.put(url, {
        // room: "",
        officeroom:"",
        id: editModel.id, 
        name: editModel.name,
        switchname: editModel.switch
      }, {
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        }
      });
      queryParameters.get("place")=="home" ? fetchHomeAppliances(roomID) : fetchOfficeAppliances(roomID)
      setIsEditModalOpen(false);
    } catch (error) {
      console.error('Error updating appliance:', error);
    }
  };

  // const handleEditSubmit = async (e) => {
  //   e.preventDefault();
  //   try {
  //     const roomID = queryParameters.get("roomId");
  //     const response = await Axios.put(`/api/homeroom/update_home_appliance/${roomID}`, {
  //       room:" ",
  //       name: editModel.name,
  //       switchname: editModel.switch
  //     }, {
  //       headers: {
  //         'Authorization': `Token ${token}`,
  //         'Content-Type': 'application/json'
  //       }
  //     });
  //     fetchHomeAppliances(roomID);
  //     setIsEditModalOpen(false);
  //   } catch (error) {
  //     console.error('Error updating appliance:', error);
  //   }
  // };

  const handleEditModalOpen = (appliance) => {
    queryParameters.get("place") === "home"?
    setEditModel({
      id: appliance.id,
      name: appliance.appliancename,
      switch: appliance.switchname
    }):
    setEditModel({
      id: appliance.appliance_id,
      name: appliance.appliance_name,
      switch: appliance.switch_name
    });
    setIsEditModalOpen(true);
  };

  const handleEditModalClose = () => {
    setIsEditModalOpen(false);
  };

  const openAddModal = () => {
    setIsAddModalOpen(true);
  };

  const closeAddModal = () => {
    setIsAddModalOpen(false);
  };



  const changeSwitchStatus=async(status,appliance_id)=>{
    const room_id = queryParameters.get("roomId");
    let url=`home/appliance_status/create/${room_id}/${appliance_id}/`;
    const token = localStorage.getItem('token');  
    const response = await Axios.post(url, {
      status:status?"on":"off"  
    }, {
      headers: {
        'Authorization': `Token ${token}`,
        'Content-Type': 'application/json'
      }
    });
  }
  const changeSwitch = async (status, appliance_id) => {
    const office_id = queryParameters.get("roomId");
    console.log(office_id, appliance_id);
    const url = `office/appliance_status/create/${office_id}/${appliance_id}/`;
    const token = localStorage.getItem('token');
    try {
      const response = await Axios.post(url, {
        status: status ? "on" : "off"
      }, {
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json'
        }
      });
      if (response.status === 200) {
        // fetchRooms();
        toast.success('Appliance status updated successfully!');
      } else {
        toast.error('Failed to update appliance status');
      }
    } catch (error) {
      toast.error('Error updating appliance status: ' + error.message);
    }
  };
  return (
    <Grid container spacing={2} sx={{ backgroundColor: "black", height: "100vh" }}>
      <Grid item xs={12} sx={{ height: "25%",display: 'flex', justifyContent: 'space-between',margin:"30px"}}>
      <Grid item xs={6} sx={{display:"flex",justifyContent:"flex-start"}}>
        <Typography sx={{ color: "white" }} variant="h4">{queryParameters.get("roomtype")}</Typography>
        </Grid>
        <Grid item xs={6} sx={{ display: "flex", justifyContent: "flex-end", flexDirection: "column", alignItems: "flex-end" }}>
  <Button variant="contained" color="primary" onClick={openAddModal}>
    Add Appliance
  </Button>
  <Box sx={{ mt: 1, display: "flex", flexDirection: "row", gap: 1 }}>
    <EditIcon sx={{ color: "white" }} />
    <DeleteIcon sx={{ color: "white" }} />
  </Box>
</Grid>

        
        </Grid>
        
        <AddApplianceModal isOpen={isAddModalOpen} onClose={closeAddModal} onSave={handleSubmit} />
        <Modal sx={{ backgroundColor: "#4d4737" }}
          open={isEditModalOpen}
          onRequestClose={handleEditModalClose}
          style={customStyles}
          contentLabel="Edit Appliance Modal"
        >
          <div>
            <CloseIcon onClick={handleEditModalClose} style={{ position: 'absolute', top: 10, right: 10, cursor: 'pointer', color: "white" }} />
            <form onSubmit={handleEditSubmit} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
              <input
                type="text"
                placeholder="Switch Name"
                value={editModel.switch}
                onChange={(e) => setEditModel({ ...editModel, switch: e.target.value })}
                style={{
                  width: '80%',
                  padding: '10px',
                  marginTop: '20px',
                  borderRadius: '5px',
                  border: '1px solid #ccc',
                  fontSize: '16px',
                }}
              />
              <input
                type="text"
                placeholder="Appliances Name"
                value={editModel.name}
                onChange={(e) => setEditModel({ ...editModel, name: e.target.value })}
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
          }}  >Submit</button>
            </form>
          </div>
        </Modal>
      
      <Grid item container xs={12} spacing={2} justifyContent="center" sx={{ backgroundColor: "black", height: "100vh" }}>
          {appliances.map((appliance,index) => (
            <Grid key={index+1} item xs={12} sm={6} md={4} sx={{margin:"2px"}}>
            <Card sx={{ minWidth: 250, display: 'flex', flexDirection: 'column', justifyContent: 'space-between', cursor: 'pointer',background: "linear-gradient(transparent, #387e8a 100%), linear-gradient(transparent, white 100%)",border:"1px solid #fff"}}>
            <CardContent>
                <Typography variant="h6" sx={{color:"white"}}>{appliance.appliancename}</Typography>
                <Switch defaultChecked onChange={(e)=>{changeSwitchStatus(e.target.checked,appliance.id)}} />
                        <Box sx={{display:"flex",justifyContent:"flex-end"}}>
                        <EditIcon sx={{color:"black"}} onClick={() => handleEditModalOpen(appliance)} />
                        <DeleteIcon onClick={() => handleHomeApplianceDelete(appliance)} sx={{color:"black"}} /> 

                        {/* <DeleteIcon onClick={() => handleDeleteRoom(item.room_id)} sx={{color:"black"}} />  */}
                        </Box>                     
                    </CardContent>
              </Card>
            </Grid>
          ))}
      </Grid>

      <Grid item container xs={12} spacing={2} justifyContent="center">
          {officeappliances.map((appliance,index) => (
            <Grid key={index+1} item xs={12} sm={6} md={4} onClick={() => handleEditModalOpen(appliance)}>
            <Card sx={{ minWidth: 250, display: 'flex',   flexDirection: 'column', justifyContent: 'space-between', cursor: 'pointer',background: "linear-gradient(transparent, #387e8a 100%), linear-gradient(transparent, white 100%)",border:"1px solid #fff"}}>
                <CardContent>       
                <Typography variant="h6" sx={{color:"black"}}>{appliance.appliance_name}</Typography>
                   <Switch defaultChecked onChange={(e)=>{changeSwitch(e.target.checked,appliance.appliance_id)}} />
                        <Box sx={{display:"flex",justifyContent:"flex-end"}}>
                        <EditIcon sx={{color:"black"}} onClick={() => handleEditModalOpen(appliance)} />
                        </Box>                     
                    </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Grid>
    
  );
};

export default Room;
