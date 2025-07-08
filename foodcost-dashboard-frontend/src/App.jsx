import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import logo from './assets/Datadash_logo.png';
import AnimatedBackground from './components/AnimatedBackground';
import FAQ from './components/FAQ';

// Tema personalizzato
const theme = createTheme({
  palette: {
    primary: { main: '#007BFF' },
    secondary: { main: '#00D084' },
  },
});

export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ position: 'relative', width: '100%', height: '100vh', overflow: 'hidden' }}>
        {/* Background animato */}
        <AnimatedBackground />

        {/* Header */}
        <Box
          sx={{
            position: 'absolute',
            top: '20px',
            width: '100%',
            px: '30%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          <Box component="img" src={logo} alt="DataDash Logo" sx={{ width: '200px', transform: 'none' }} />
          <Button variant="contained" color="primary" sx={{ textTransform: 'none', fontWeight: 700, fontSize: '0.875rem', px: 3, py: 1, borderRadius: '4px' }}>
            Accedi
          </Button>
        </Box>

        {/* Messaggio centrale */}
        <Box
          sx={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            width: '50%',
            textAlign: 'center',
          }}
        >
          <Typography
            variant="h2"
            component="h1"
            sx={{
              fontWeight: 700,
              color: '#FFFFFF',
              fontSize: ['2rem', '3rem', '4rem'],
            }}
          >
            Taglia gli sprechi, non i sapori: DataDash per la tua ristorazione
          </Typography>
          {/* Sottotitolo */}
          <Typography
            variant="h5"
            component="h2"
            sx={{
              mt: 2,
              fontWeight: 400,
              color: '#FFFFFF',
              fontSize: ['1rem', '1.25rem', '1.5rem'],
            }}
          >
            Inizia il tuo mese gratuito, disdici quando vuoi
          </Typography>
        </Box>

        {/* Sezione FAQ */}
        <Box
          sx={{
            position: '',
            bottom: 100,
            width: '100%',
            bgcolor: 'rgba(0, 0, 0, 0.7)',
            py: 6,
          }}
        >
          <FAQ />
        </Box>
      </Box>
    </ThemeProvider>
  );
}
