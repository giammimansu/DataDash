import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AppLayout from './layout/AppLayout';
import Dashboard from './pages/Dashboard';
import ImportCSV from './pages/ImportCSV';
import InventoryPage from './pages/InventoryPage';
import RidersPage from './pages/RidersPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="import" element={<ImportCSV />} />
          <Route path="inventory" element={<InventoryPage />} />
          <Route path="riders" element={<RidersPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
