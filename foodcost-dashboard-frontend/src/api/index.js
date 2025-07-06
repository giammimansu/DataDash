import axios from 'axios';

export const api = axios.create({
  baseURL: 'http://127.0.0.1:8000'
});

// ORDINI
export const importOrders = file => {
  const form = new FormData();
  form.append('file', file);
  return api.post('/orders/import-csv/', form);
};
export const exportOrders = () =>
  api.get('/orders/export-csv/', { responseType: 'blob' });

// INGREDIENTI
export const importIngredients = file => {
  const form = new FormData();
  form.append('file', file);
  return api.post('/ingredients/import-costs-csv/', form);
};
export const exportIngredients = () =>
  api.get('/ingredients/export-costs-csv/', { responseType: 'blob' });

// LETTURA DATI per Dashboard
export const fetchOrders = (params = {}) =>
  api.get('/orders/', { params });

export const fetchIngredients = (params = {}) =>
  api.get('/ingredients/', { params });

// COSTI CIBO
export const fetchFoodCosts = () =>
  api.get('/products/food-cost/');



// PRODUCTS
export function importProducts(file) {
  const data = new FormData();
  data.append('file', file);
  return api.post('/products/import-csv/', data, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
}
export function exportProducts() {
  return api.get('/products/export-csv/', { responseType: 'blob' });
}

// RECIPES
export function importRecipes(file) {
  const data = new FormData();
  data.append('file', file);
  return api.post('/recipes/import-csv/', data, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
}
export function exportRecipes() {
  return api.get('/recipes/export-csv/', { responseType: 'blob' });
}

// INVENTORY
export function importInventory(file) {
  const data = new FormData();
  data.append('file', file);
  return api.post('/inventory/import-csv/', data, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
}
export function exportInventory() {
  return api.get('/inventory/export-csv/', { responseType: 'blob' });
}

// RIDERS
export function importRiders(file) {
  const data = new FormData();
  data.append('file', file);
  return api.post('/riders/import-csv/', data, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
}
export function exportRiders() {
  return api.get('/riders/export-csv/', { responseType: 'blob' });
}


// Margine lordo per prodotto
export const fetchProductMargin = () =>
  api.get('/products/margine-lordo/');
