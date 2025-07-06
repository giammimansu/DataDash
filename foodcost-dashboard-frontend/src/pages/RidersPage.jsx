import React, { useEffect, useState } from 'react';
import DataTable from '../components/DataTable';
import ChartContainer from '../components/ChartContainer';
import { fetchRiders, fetchRiderPerformance } from '../api/api';

export default function RidersPage() {
  const [riders, setRiders] = useState([]);
  const [perf, setPerf] = useState([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  useEffect(() => {
    async function load() {
      const r = await fetchRiders();
      setRiders(r.data.map((x, i) => ({ id: i, name: x.name, deliveries: x.deliveries })));
      const p = await fetchRiderPerformance();
      setPerf(p.data);
    }
    load();
  }, []);

  const columns = [
    { field: 'name', headerName: 'Rider' },
    { field: 'deliveries', headerName: 'Consegne' }
  ];

  return (
    <>
      <ChartContainer title="Performance Rider">
        {/* qui potresti mettere un grafico a barre con perf */}
      </ChartContainer>
      <DataTable
        columns={columns}
        rows={riders}
        page={page}
        setPage={setPage}
        rowsPerPage={rowsPerPage}
        setRowsPerPage={setRowsPerPage}
      />
    </>
  );
}
