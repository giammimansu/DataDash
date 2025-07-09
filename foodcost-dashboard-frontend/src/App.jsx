import React, { useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import LandingPage from './pages/LandingPage';
import Home from './pages/Home';

const theme = createTheme({ palette: { primary: { main: '#007BFF' }, secondary: { main: '#00D084' } } });

export default function App() {
  const [user, setUser] = useState(null);

  const handleAuthSuccess = (userData, token) => {
    setUser(userData);
    localStorage.setItem('access_token', token);
  };

  return (
    <ThemeProvider theme={theme}>
      {user ? <Home /> : <LandingPage onAuthSuccess={handleAuthSuccess} />}
    </ThemeProvider>
  );
}
