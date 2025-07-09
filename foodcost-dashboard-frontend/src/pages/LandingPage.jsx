import React, { useState } from 'react';
import { Box, Button, Drawer, Typography } from '@mui/material';
import logo from '../assets/Datadash_logo.png';
import AnimatedBackground from '../components/AnimatedBackground';
import FAQ from '../components/FAQ';
import LoginPage from './Login';
import RegisterPage from './Register';

export default function LandingPage({ onAuthSuccess }) {
  const [loginOpen, setLoginOpen] = useState(false);
  const [registerOpen, setRegisterOpen] = useState(false);

  const handleLoginOpen = () => setLoginOpen(true);
  const handleLoginClose = () => setLoginOpen(false);
  const handleRegisterOpen = () => setRegisterOpen(true);
  const handleRegisterClose = () => setRegisterOpen(false);
  const handleSwitchToRegister = () => {
    setLoginOpen(false);
    setRegisterOpen(true);
  };

  return (
    <Box sx={{ position: 'relative', width: '100%', height: '100vh', overflowY: 'auto' }}>
      <AnimatedBackground />

      {/* Central text */}
      <Box sx={{
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: ['80%', '60%', '40%'],
        textAlign: 'center',
        color: '#FFFFFF',
        px: 2
      }}>
        <Typography variant="h2" component="h1" sx={{ fontWeight: 700, fontSize: ['2rem','3rem','4rem'] }}>
          Taglia gli sprechi, non i sapori: DataDash per la tua ristorazione
        </Typography>
        <Typography variant="h5" component="h2" sx={{ mt: 2, fontWeight: 400, fontSize: ['1rem','1.25rem','1.5rem'] }}>
          Inizia il tuo mese gratuito, disdici quando vuoi
        </Typography>
      </Box>

      {/* Header with logo and buttons */}
      <Box sx={{ position: 'absolute', top: 20, width: '100%', px: '30%', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Box component="img" src={logo} alt="DataDash Logo" sx={{ width: 200 }} />
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button variant="contained" color="primary" onClick={handleLoginOpen} sx={{ textTransform: 'none', fontWeight: 700, fontSize: '0.875rem', px:3, py:1, borderRadius:4 }}>
            Accedi
          </Button>
          <Button variant="outlined" color="secondary" onClick={handleRegisterOpen} sx={{ textTransform: 'none', fontWeight:700, fontSize:'0.875rem', px:3, py:1, borderRadius:4 }}>
            Registrati
          </Button>
        </Box>
      </Box>

      {/* FAQ section */}
      <Box sx={{ position: 'absolute', top: '80%', width: '100%', bgcolor: 'rgba(0, 0, 0, 0.7)', py: 6 }}>
        <FAQ />
      </Box>

      {/* Drawers */}
      <Drawer anchor="right" open={loginOpen} onClose={handleLoginClose} PaperProps={{ sx:{ width: ['80%','60%','30%'], backgroundColor: 'transparent', boxShadow: 'none'} }} transitionDuration={500}>
        {/* Pass onAuthSuccess directly so arguments align */}
        <LoginPage
          onLogin={onAuthSuccess}
          onClose={handleLoginClose}
          onSwitchToRegister={handleSwitchToRegister}
        />
      </Drawer>
      <Drawer anchor="right" open={registerOpen} onClose={handleRegisterClose} PaperProps={{ sx:{ width:['80%','60%','30%'], backgroundColor:'transparent', boxShadow:'none'}}} transitionDuration={500}>
        <RegisterPage
          onRegister={onAuthSuccess}
          onClose={handleRegisterClose}
        />
      </Drawer>
    </Box>
  );
}