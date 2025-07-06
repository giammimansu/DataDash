// src/App.js
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import theme from './theme/customTheme';
import AppLayout from './layout/AppLayout';
import Dashboard from './pages/Dashboard';
import ImportCSV from './pages/ImportCSV';
import InventoryPage from './pages/InventoryPage';
import RidersPage from './pages/RidersPage';

export default function App() {
  return (
    <ThemeProvider theme={theme}>
      <BrowserRouter>
        <Routes>
          {/* AppLayout contiene AppBar, Drawer e Outlet */}
          <Route element={<AppLayout />}>
            <Route path="/" element={<Dashboard />} />
            <Route path="import" element={<ImportCSV />} />
            <Route path="inventory" element={<InventoryPage />} />
            <Route path="riders" element={<RidersPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}
