import React, { useEffect, useState } from 'react';
import { Grid } from '@mui/material';
import MetricCard from '../components/MetricCard';
import ChartContainer from '../components/ChartContainer';
import { fetchOrders, fetchFoodCosts } from '../api/api';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';

export default function Dashboard() {
  const [kpi, setKpi] = useState({ totalSales: 0, avgFoodCost: 0 });
  const [trend, setTrend] = useState([]);

  useEffect(() => {
    async function load() {
      const orders = await fetchOrders();
      const cost = await fetchFoodCosts();
      setKpi({
        totalSales: orders.data.length,
        avgFoodCost: (cost.data.reduce((a,b)=>a+b.value,0)/cost.data.length).toFixed(2)
      });
      // mock trend data
      setTrend(orders.data.map(o=>({ date: o.date, value: o.total })));
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
        <ChartContainer title="Andamento Vendite">
          <ResponsiveContainer width='100%' height={200}>
            <LineChart data={trend} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="value" stroke="#1976d2" />
            </LineChart>
          </ResponsiveContainer>
        </ChartContainer>
      </Grid>
    </Grid>
  );
}
