import React, { useEffect, useState } from 'react';
import { Grid } from '@mui/material';
import MetricCard from '../components/MetricCard';
import ChartContainer from '../components/ChartContainer';
import { fetchOrders, fetchFoodCosts } from '../api';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';

export default function Dashboard() {
  const [kpi, setKpi] = useState({ totalSales: 0, avgFoodCost: 0 });
  useEffect(() => {
    async function load() {
      const orders = await fetchOrders();
      const cost = await fetchFoodCosts();
      setKpi({
        totalSales: orders.data.length,
        avgFoodCost: cost.data.reduce((a,b)=>a+b.value,0)/cost.data.length
      });
    }
    load();
  }, []);

  return (
    <Grid container spacing={2}>
      <Grid item xs={12} md={4}>
        <MetricCard
          icon={ShoppingCartIcon}
          title="Ordini Totali"
          value={kpi.totalSales}
          subtitle="Numero di ordini processati"
        />
      </Grid>
      <Grid item xs={12} md={8}>
        <ChartContainer title="Andamento Food Cost">
          {/* qui potresti mettere un Recharts LineChart */}
          {/* <LineChart data={…}/> */}
        </ChartContainer>
      </Grid>
    </Grid>
  );
}
