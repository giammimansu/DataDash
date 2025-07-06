// src/pages/Dashboard.js
import React, { useEffect, useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow
} from '@mui/material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from 'recharts';

import { fetchOrders, fetchIngredients, fetchFoodCosts, fetchProductMargin } from '../api/api';



export default function Dashboard() {
  const [orders, setOrders] = useState([]);
  const [ingredients, setIngredients] = useState([]);
  const [foodCosts, setFoodCosts] = useState([]);
  const [productMargin, setProductMargin] = useState([]);

  useEffect(() => {
    fetchOrders().then(res => setOrders(res.data));
    fetchIngredients().then(res => setIngredients(res.data));
    fetchFoodCosts().then(res => setFoodCosts(res.data));
    fetchProductMargin().then(res => setProductMargin(res.data));
  }, []);

  // Aggrega vendite per fascia oraria
  const salesByHour = orders.reduce((acc, o) => {
    const hour = new Date(o.timestamp).getHours();
    acc[hour] = (acc[hour] || 0) + o.quantity;
    return acc;
  }, {});
  const salesData = Object.entries(salesByHour).map(([hour, qty]) => ({ hour, qty }));

  return (
    <Box sx={{ p: 4, display: 'grid', gap: 4 }}>
      <Typography variant="h4">Dashboard</Typography>

      <Paper sx={{ p: 2 }}>
        <Typography variant="h6">Vendite per Fascia Oraria</Typography>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={salesData}>
            <XAxis dataKey="hour" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="qty" />
          </BarChart>
        </ResponsiveContainer>
      </Paper>

      <Paper sx={{ p: 2 }}>
        <Typography variant="h6">Costi Ingredienti</Typography>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Ingredient</TableCell>
              <TableCell align="right">Unit Cost</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {ingredients.map(ing => (
              <TableRow key={ing.id}>
                <TableCell>{ing.name}</TableCell>
                <TableCell align="right">{ing.unit_cost.toFixed(2)}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Paper>

      <Paper sx={{ p: 2 }}>
        <Typography variant="h6">Food Cost per Prodotto</Typography>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Product ID</TableCell>
              <TableCell align="right">Food Cost</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {foodCosts.map(fc => (
              <TableRow key={fc.product_id}>
                <TableCell>{fc.product_id}</TableCell>
                <TableCell align="right">{fc.food_cost.toFixed(2)}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Paper>

      <Paper sx={{ p: 2 }}>
  <Typography variant="h6">Margine Lordo per Prodotto</Typography>
  <Table>
    <TableHead>
      <TableRow>
        <TableCell>Product ID</TableCell>
        <TableCell align="right">Prezzo Medio</TableCell>
        <TableCell align="right">Food Cost</TableCell>
        <TableCell align="right">Margine Lordo</TableCell>
      </TableRow>
    </TableHead>
    <TableBody>
      {productMargin.map(pm => (
        <TableRow key={pm.product_id}>
          <TableCell>{pm.product_id}</TableCell>
          <TableCell align="right">{pm.avg_price.toFixed(2)}</TableCell>
          <TableCell align="right">{pm.food_cost.toFixed(2)}</TableCell>
          <TableCell
            align="right"
            sx={{ color: pm.margin >= 0 ? 'green' : 'red' }}
          >
            {pm.margin.toFixed(2)}
          </TableCell>
        </TableRow>
      ))}
    </TableBody>
  </Table>
</Paper>

    </Box>
  );
}
