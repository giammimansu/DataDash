import React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';

export default function Home() {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div">
          DataDash
        </Typography>
      </Toolbar>
    </AppBar>
  );
}
