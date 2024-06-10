const fetchRooms = async () => {
  try {
    const token = localStorage.getItem('token');
    const user_id = localStorage.getItem('userId');
    const response = await Axios.get(`api/get-office-room/${user_id}`, {
      headers: {
        'Authorization': `Token ${token}`,
      }
    });

    console.log(response.data); // Log the entire response data to inspect it
    const officeRooms = response.data.office_rooms;

    if (response.status === 200 && Array.isArray(officeRooms)) {
      setRooms(officeRooms);
    } else {
      toast.error('Failed to fetch rooms or invalid data format');
    }
  } catch (error) {
    toast.error('Error fetching rooms: ' + error.message);
  }
};
