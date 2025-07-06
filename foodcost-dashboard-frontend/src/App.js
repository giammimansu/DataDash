// src/App.js
import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { AppBar, Toolbar, Button, Container } from '@mui/material';
import ImportCSV from './pages/ImportCSV';
import Dashboard from './pages/Dashboard';

function App() {
  return (
    <BrowserRouter>
      <AppBar position="static">
        <Toolbar>
          <Button color="inherit" component={Link} to="/import">
            Import CSV
          </Button>
          <Button color="inherit" component={Link} to="/dashboard">
            Dashboard
          </Button>
        </Toolbar>
      </AppBar>

      <Container sx={{ mt: 4 }}>
        <Routes>
          <Route path="/import" element={<ImportCSV />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="*" element={<ImportCSV />} />
        </Routes>
      </Container>
    </BrowserRouter>
  );
}

export default App;
