import React from 'react';
import Register from './component/Register';
import Login from './component/Login'
import Dashboard from './component/Dashboard';
import Rooms from './component/Rooms';
// import LivingRoom from './component/LivingRoom';
import { BrowserRouter, Route, Routes,Navigate } from 'react-router-dom';
import Home from './component/Home';
import Office from './component/Office';
import Adminlogin from './Admin/login';
import Admin from './Admin/admin_dashboard'
import User from './Admin/User';
import UserDetails from './Admin/Userdetails';
function App() {
  const isAuthenticated=localStorage.getItem("token");
  return (
    <BrowserRouter>
    <Routes>
      <Route path='/' element={<Login />} />
      <Route path='/register' element={<Register />} />
      {/* <Route path='/dashboard' element={isAuthenticated ? <Dashboard /> : Navigate("/")} /> */}
      <Route path='/dashboard' element={isAuthenticated ? <Dashboard /> : <Navigate to="/" />} />
      <Route path='/admin_dashboard' element={isAuthenticated ? <Admin /> : <Navigate to="/" />} />

      {/* <Route path='/rooms:roomty' element={<Rooms />} /> */}
      <Route path='/home' element={<Home />} />
      <Route path='/office' element={<Office />} />
      <Route path='/rooms' element={<Rooms />} />
      <Route path='/user' element={<User />} />
      <Route path='/login' element={<Adminlogin />} />
      <Route path="/user/:id" element={<UserDetails />} />

    </Routes>
    </BrowserRouter>
  );
}

export default App;
