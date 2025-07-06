import React, { useState } from 'react';
import { Box, Card, CardContent, CardActions, Button, Typography } from '@mui/material';
import {
  importOrders,
  importIngredients,
  importProducts,
  importRecipes,
  importInventory,
  importRiders,
  exportOrders,
  exportIngredients,
  exportProducts,
  exportRecipes,
  exportInventory,
  exportRiders
} from '../api/api';

export default function ImportCSV() {
  const [files, setFiles] = useState({});

  const handleChange = (key) => (e) => {
    setFiles(prev => ({ ...prev, [key]: e.target.files[0] }));
  };

  const handleImport = async (key, importFn, label) => {
    if (!files[key]) return alert(`Seleziona un file ${label}`);
    try {
      const res = await importFn(files[key]);
      alert(`Importati ${res.data.length} ${label}`);
    } catch {
      alert(`Errore import ${label}`);
    }
  };

  const downloadCSV = async (exportFn, filename, errorLabel) => {
    try {
      const res = await exportFn();
      const url = window.URL.createObjectURL(new Blob([res.data], { type: 'text/csv' }));
      const a = document.createElement('a');
      a.href = url;
      a.setAttribute('download', filename);
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch {
      alert(errorLabel);
    }
  };

  const entities = [
    { key: 'orders', importFn: importOrders, exportFn: exportOrders, label: 'ordini', downloadName: 'orders_export.csv' },
    { key: 'ingredients', importFn: importIngredients, exportFn: exportIngredients, label: 'ingredienti', downloadName: 'ingredient_costs_export.csv' },
    { key: 'products', importFn: importProducts, exportFn: exportProducts, label: 'prodotti', downloadName: 'products_export.csv' },
    { key: 'recipes', importFn: importRecipes, exportFn: exportRecipes, label: 'ricette', downloadName: 'recipes_export.csv' },
    { key: 'inventory', importFn: importInventory, exportFn: exportInventory, label: 'movimenti magazzino', downloadName: 'inventory_export.csv' },
    { key: 'riders', importFn: importRiders, exportFn: exportRiders, label: 'riders', downloadName: 'riders_export.csv' }
  ];

  return (
    <Box sx={{ p: 4, display: 'grid', gap: 4 }}>
      {entities.map(ent => (
        <Card key={ent.key}>
          <CardContent>
            <Typography variant="h6">Import {ent.label.charAt(0).toUpperCase() + ent.label.slice(1)} (CSV)</Typography>
            <input type="file" accept=".csv" onChange={handleChange(ent.key)} />
          </CardContent>
          <CardActions>
            <Button variant="contained" onClick={() => handleImport(ent.key, ent.importFn, ent.label)}>Carica {ent.label}</Button>
            <Button variant="outlined" onClick={() => downloadCSV(ent.exportFn, ent.downloadName, `Errore download ${ent.label}`)}>Scarica {ent.label}</Button>
          </CardActions>
        </Card>
      ))}
    </Box>
  );
}
