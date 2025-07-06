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
} from '../api';

export default function ImportCSV() {
  const [ordersFile, setOrdersFile] = useState(null);
  const [ingredientsFile, setIngredientsFile] = useState(null);
  const [productsFile, setProductsFile] = useState(null);
  const [recipesFile, setRecipesFile] = useState(null);
  const [inventoryFile, setInventoryFile] = useState(null);
  const [ridersFile, setRidersFile] = useState(null);

  const handleImport = async (file, importFn, label) => {
    if (!file) return alert(`Seleziona un file ${label}`);
    try {
      const res = await importFn(file);
      alert(`Importati ${res.data.length} ${label}`);
    } catch (e) {
      console.error(e);
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
    } catch (e) {
      console.error(e);
      alert(errorLabel);
    }
  };

  return (
    <Box sx={{ p: 4, display: 'grid', gap: 4 }}>
      {/* Orders */}
      <Card>
        <CardContent>
          <Typography variant="h6">Import Ordini (CSV)</Typography>
          <input
            type="file"
            accept=".csv"
            onChange={e => setOrdersFile(e.target.files[0])}
          />
        </CardContent>
        <CardActions>
          <Button variant="contained" onClick={() => handleImport(ordersFile, importOrders, 'ordini')}>Carica Ordini</Button>
          <Button variant="outlined" onClick={() => downloadCSV(exportOrders, 'orders_export.csv', 'Errore download ordini')}>Scarica Ordini</Button>
        </CardActions>
      </Card>

      {/* Ingredients */}
      <Card>
        <CardContent>
          <Typography variant="h6">Import Costi Ingredienti (CSV)</Typography>
          <input
            type="file"
            accept=".csv"
            onChange={e => setIngredientsFile(e.target.files[0])}
          />
        </CardContent>
        <CardActions>
          <Button variant="contained" onClick={() => handleImport(ingredientsFile, importIngredients, 'ingredienti')}>Carica Ingredienti</Button>
          <Button variant="outlined" onClick={() => downloadCSV(exportIngredients, 'ingredient_costs_export.csv', 'Errore download ingredienti')}>Scarica Ingredienti</Button>
        </CardActions>
      </Card>

      {/* Products */}
      <Card>
        <CardContent>
          <Typography variant="h6">Import Prodotti (CSV)</Typography>
          <input
            type="file"
            accept=".csv"
            onChange={e => setProductsFile(e.target.files[0])}
          />
        </CardContent>
        <CardActions>
          <Button variant="contained" onClick={() => handleImport(productsFile, importProducts, 'prodotti')}>Carica Prodotti</Button>
          <Button variant="outlined" onClick={() => downloadCSV(exportProducts, 'products_export.csv', 'Errore download prodotti')}>Scarica Prodotti</Button>
        </CardActions>
      </Card>

      {/* Recipes */}
      <Card>
        <CardContent>
          <Typography variant="h6">Import Ricette (CSV)</Typography>
          <input
            type="file"
            accept=".csv"
            onChange={e => setRecipesFile(e.target.files[0])}
          />
        </CardContent>
        <CardActions>
          <Button variant="contained" onClick={() => handleImport(recipesFile, importRecipes, 'ricette')}>Carica Ricette</Button>
          <Button variant="outlined" onClick={() => downloadCSV(exportRecipes, 'recipes_export.csv', 'Errore download ricette')}>Scarica Ricette</Button>
        </CardActions>
      </Card>

      {/* Inventory */}
      <Card>
        <CardContent>
          <Typography variant="h6">Import Movimenti Magazzino (CSV)</Typography>
          <input
            type="file"
            accept=".csv"
            onChange={e => setInventoryFile(e.target.files[0])}
          />
        </CardContent>
        <CardActions>
          <Button variant="contained" onClick={() => handleImport(inventoryFile, importInventory, 'movimenti magazzino')}>Carica Magazzino</Button>
          <Button variant="outlined" onClick={() => downloadCSV(exportInventory, 'inventory_export.csv', 'Errore download magazzino')}>Scarica Magazzino</Button>
        </CardActions>
      </Card>

      {/* Riders */}
      <Card>
        <CardContent>
          <Typography variant="h6">Import Riders (CSV)</Typography>
          <input
            type="file"
            accept=".csv"
            onChange={e => setRidersFile(e.target.files[0])}
          />
        </CardContent>
        <CardActions>
          <Button variant="contained" onClick={() => handleImport(ridersFile, importRiders, 'riders')}>Carica Riders</Button>
          <Button variant="outlined" onClick={() => downloadCSV(exportRiders, 'riders_export.csv', 'Errore download riders')}>Scarica Riders</Button>
        </CardActions>
      </Card>
    </Box>
  );
}
