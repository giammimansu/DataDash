import React, { useEffect, useState } from 'react';
import DataTable from '../components/DataTable';
import ChartContainer from '../components/ChartContainer';
import { fetchInventory } from '../api/api';

export default function InventoryPage() {
  const [rows, setRows] = useState([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  useEffect(() => {
    async function load() {
      const res = await fetchInventory();
      // assume API returns [{ ingredient, quantity }]
      setRows(res.data.map((r, idx) => ({ id: idx, ...r })));  
    }
    load();
  }, []);

  const columns = [
    { field: 'ingredient', headerName: 'Ingrediente' },
    { field: 'quantity', headerName: 'Quantità' }
  ];

  return (
    <ChartContainer title="Scorta Residua">
      <DataTable
        columns={columns}
        rows={rows}
        page={page}
        setPage={setPage}
        rowsPerPage={rowsPerPage}
        setRowsPerPage={setRowsPerPage}
      />
    </ChartContainer>
  );
}

