"""
FastAPI - Food Cost Dashboard API

Gestione CRUD, import/export CSV e dashboard analytics per:
- Ingredienti
- Prodotti
- Ricette
- Ordini
- Magazzino
- Rider

Tutto pronto per sviluppo locale e futura estensione multi-tenant/cloud.
"""

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from collections import defaultdict
from io import StringIO
from datetime import datetime
import csv

from . import models, schemas, crud
from .database import SessionLocal, engine

# --------------------------
# INIT FastAPI e CORS policy
# --------------------------
app = FastAPI(title="Food Cost Dashboard API", version="0.1")

origins = ["http://localhost:3000"]  # frontend in dev su localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crea tutte le tabelle al primo avvio (sviluppo)
models.Base.metadata.create_all(bind=engine)

# Dependency: crea una sessione DB per ogni request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================================
# CRUD ENDPOINTS - GESTIONE DATI DI BASE
# =========================================

# ---- INGREDIENTI ----

@app.post("/ingredients/", response_model=schemas.Ingredient)
def create_ingredient(ingredient: schemas.IngredientCreate, db: Session = Depends(get_db)):
    """Crea un nuovo ingrediente."""
    return crud.create_ingredient(db, ingredient)

@app.get("/ingredients/", response_model=list[schemas.Ingredient])
def read_ingredients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Restituisce tutti gli ingredienti, paginati."""
    return crud.get_ingredients(db, skip=skip, limit=limit)

@app.get("/ingredients/{ingredient_id}", response_model=schemas.Ingredient)
def read_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    """Restituisce un singolo ingrediente per ID."""
    db_ing = crud.get_ingredient(db, ingredient_id)
    if not db_ing:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return db_ing

@app.put("/ingredients/{ingredient_id}", response_model=schemas.Ingredient)
def update_ingredient(ingredient_id: int, ingredient: schemas.IngredientCreate, db: Session = Depends(get_db)):
    """Aggiorna un ingrediente esistente (nome/costo)."""
    db_ing = crud.update_ingredient(db, ingredient_id, ingredient)
    if not db_ing:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return db_ing

@app.delete("/ingredients/{ingredient_id}", status_code=204)
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    """Elimina un ingrediente per ID."""
    crud.delete_ingredient(db, ingredient_id)
    return

# ---- PRODOTTI ----

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """Crea un nuovo prodotto (piatto/voce menu)."""
    return crud.create_product(db, product)

@app.get("/products/", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Restituisce tutti i prodotti (paginati)."""
    return crud.get_products(db, skip=skip, limit=limit)

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    """Restituisce un singolo prodotto per ID."""
    db_prod = crud.get_product(db, product_id)
    if not db_prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_prod

@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """Aggiorna nome di un prodotto."""
    db_prod = crud.update_product(db, product_id, product)
    if not db_prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_prod

@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Elimina un prodotto."""
    crud.delete_product(db, product_id)
    return

# ---- RICETTE ----

@app.post("/recipes/", response_model=schemas.Recipe)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    """Aggiungi una riga ricetta (ingredienti e quantità per prodotto)."""
    return crud.create_recipe(db, recipe)

@app.get("/recipes/", response_model=list[schemas.Recipe])
def read_recipes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Tutte le righe ricetta (ingredienti usati nei prodotti)."""
    return crud.get_recipes(db, skip=skip, limit=limit)

@app.delete("/recipes/{recipe_id}", status_code=204)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """Elimina una riga ricetta."""
    crud.delete_recipe(db, recipe_id)
    return

# ---- ORDINI ----

@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    """Crea un nuovo ordine (vendita prodotto, opzionalmente rider)."""
    return crud.create_order(db, order)

@app.get("/orders/", response_model=list[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Tutti gli ordini (vendite), paginati."""
    return crud.get_orders(db, skip=skip, limit=limit)

@app.get("/orders/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    """Ordine singolo per ID."""
    db_ord = crud.get_order(db, order_id)
    if not db_ord:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_ord

@app.delete("/orders/{order_id}", status_code=204)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """Elimina un ordine."""
    crud.delete_order(db, order_id)
    return

# ---- MAGAZZINO (CARICHI/SCARICHI) ----

@app.post("/inventory/", response_model=schemas.InventoryMovement)
def create_inventory_movement(mov: schemas.InventoryMovementCreate, db: Session = Depends(get_db)):
    """Aggiungi movimento di magazzino (carico/scarico ingrediente)."""
    return crud.create_inventory_movement(db, mov)

@app.get("/inventory/", response_model=list[schemas.InventoryMovement])
def read_inventory_movements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista movimenti di magazzino."""
    return crud.get_inventory_movements(db, skip=skip, limit=limit)

@app.delete("/inventory/{movement_id}", status_code=204)
def delete_inventory_movement(movement_id: int, db: Session = Depends(get_db)):
    """Elimina movimento magazzino."""
    crud.delete_inventory_movement(db, movement_id)
    return

# ---- RIDER ----

@app.post("/riders/", response_model=schemas.Rider)
def create_rider(rider: schemas.RiderCreate, db: Session = Depends(get_db)):
    """Crea nuovo rider (fattorino/consegna)."""
    return crud.create_rider(db, rider)

@app.get("/riders/", response_model=list[schemas.Rider])
def read_riders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Tutti i rider registrati."""
    return crud.get_riders(db, skip=skip, limit=limit)

@app.get("/riders/{rider_id}", response_model=schemas.Rider)
def read_rider(rider_id: int, db: Session = Depends(get_db)):
    """Singolo rider per ID."""
    db_r = crud.get_rider(db, rider_id)
    if not db_r:
        raise HTTPException(status_code=404, detail="Rider not found")
    return db_r

@app.put("/riders/{rider_id}", response_model=schemas.Rider)
def update_rider(rider_id: int, rider: schemas.RiderCreate, db: Session = Depends(get_db)):
    """Aggiorna nome/tempo medio consegna di un rider."""
    db_r = crud.update_rider(db, rider_id, rider)
    if not db_r:
        raise HTTPException(status_code=404, detail="Rider not found")
    return db_r

@app.delete("/riders/{rider_id}", status_code=204)
def delete_rider(rider_id: int, db: Session = Depends(get_db)):
    """Elimina un rider."""
    crud.delete_rider(db, rider_id)
    return

# =========================================
# ENDPOINTS IMPORT CSV
# =========================================

@app.post("/orders/import-csv/", response_model=list[schemas.Order])
async def import_orders_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Importa ordini da file CSV con colonne: product_id, quantity, price, rider_id, timestamp."""
    content = await file.read()
    reader = csv.DictReader(StringIO(content.decode('utf-8')))
    created = []
    for row in reader:
        data = {
            'product_id': int(row['product_id']),
            'quantity': int(row['quantity']),
            'price': float(row['price']),
            'rider_id': int(row['rider_id']) if row.get('rider_id') else None,
            'timestamp': row.get('timestamp') or None
        }
        order_in = schemas.OrderCreate(**data)
        obj = crud.create_order(db, order_in)
        created.append(obj)
    return created

@app.post("/ingredients/import-costs-csv/", response_model=list[schemas.Ingredient])
async def import_ingredient_costs_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Importa costi ingredienti da CSV: id (opz.), name, unit_cost."""
    content = await file.read()
    reader = csv.DictReader(StringIO(content.decode('utf-8')))
    results = []
    for row in reader:
        ing = crud.get_ingredient(db, int(row['id'])) if row.get('id') else \
              db.query(models.Ingredient).filter(models.Ingredient.name == row['name']).first()
        cost = float(row['unit_cost'])
        if ing:
            ing_upd = schemas.IngredientCreate(name=ing.name, unit_cost=cost)
            updated = crud.update_ingredient(db, ing.id, ing_upd)
            results.append(updated)
        else:
            new_ing = schemas.IngredientCreate(name=row['name'], unit_cost=cost)
            created = crud.create_ingredient(db, new_ing)
            results.append(created)
    return results

@app.post("/products/import-csv/", response_model=list[schemas.Product])
async def import_products_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Importa prodotti da CSV (colonna name)."""
    content = await file.read()
    reader = csv.DictReader(StringIO(content.decode('utf-8')))
    created = []
    for row in reader:
        prod_in = schemas.ProductCreate(name=row['name'])
        obj = crud.create_product(db, prod_in)
        created.append(obj)
    return created

@app.post("/recipes/import-csv/", response_model=list[schemas.Recipe])
async def import_recipes_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Importa ricette da CSV (colonne: product_id, ingredient_id, quantity)."""
    content = await file.read()
    reader = csv.DictReader(StringIO(content.decode('utf-8')))
    created = []
    for row in reader:
        rec_in = schemas.RecipeCreate(
            product_id=int(row['product_id']),
            ingredient_id=int(row['ingredient_id']),
            quantity=float(row['quantity'])
        )
        obj = crud.create_recipe(db, rec_in)
        created.append(obj)
    return created

@app.post("/inventory/import-csv/", response_model=list[schemas.InventoryMovement])
async def import_inventory_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Importa movimenti magazzino da CSV (ingredient_id, quantity, movement_type, timestamp)."""
    content = await file.read()
    reader = csv.DictReader(StringIO(content.decode('utf-8')))
    created = []
    for row in reader:
        mov_in = schemas.InventoryMovementCreate(
            ingredient_id=int(row['ingredient_id']),
            quantity=float(row['quantity']),
            movement_type=row['movement_type'],
            timestamp=row.get('timestamp') or None
        )
        obj = crud.create_inventory_movement(db, mov_in)
        created.append(obj)
    return created

@app.post("/riders/import-csv/", response_model=list[schemas.Rider])
async def import_riders_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Importa rider da CSV (colonne: name, delivery_time)."""
    content = await file.read()
    reader = csv.DictReader(StringIO(content.decode('utf-8')))
    created = []
    for row in reader:
        rider_in = schemas.RiderCreate(
            name=row['name'],
            delivery_time=float(row['delivery_time']) if row.get('delivery_time') else None
        )
        obj = crud.create_rider(db, rider_in)
        created.append(obj)
    return created

# =========================================
# DASHBOARD / KPI / AGGREGATI
# =========================================

@app.get("/products/food-cost/", response_model=list[schemas.ProductFoodCost], summary="Food cost per prodotto")
def read_food_costs(db: Session = Depends(get_db)):
    """
    Calcola il food cost per ciascun prodotto:
    somma costo ingredienti della ricetta per prodotto.
    """
    recipes = crud.get_all_recipes(db)
    ingredients = crud.get_ingredients(db, skip=0, limit=1000)
    cost_map = {ing.id: ing.unit_cost for ing in ingredients}
    prod_costs = defaultdict(float)
    for r in recipes:
        prod_costs[r.product_id] += cost_map.get(r.ingredient_id, 0) * r.quantity
    return [{"product_id": pid, "food_cost": round(cost, 2)} for pid, cost in prod_costs.items()]

@app.get("/products/margine-lordo/", response_model=list[schemas.ProductMargin], summary="Margine lordo per prodotto")
def read_product_margin(db: Session = Depends(get_db)):
    """
    Calcola il margine lordo per prodotto:
    - prezzo medio di vendita (da ordini)
    - food cost (da ricetta)
    - margine = prezzo medio - food cost
    """
    stats = db.query(
        models.Order.product_id,
        func.sum(models.Order.price).label("total_price"),
        func.sum(models.Order.quantity).label("total_qty")
    ).group_by(models.Order.product_id).all()
    ingredients = crud.get_ingredients(db, skip=0, limit=1000)
    recipes = crud.get_all_recipes(db, skip=0, limit=1000)
    cost_map = {ing.id: ing.unit_cost for ing in ingredients}
    prod_costs = defaultdict(float)
    for r in recipes:
        prod_costs[r.product_id] += cost_map.get(r.ingredient_id, 0) * r.quantity
    result = []
    for prod_id, total_price, total_qty in stats:
        avg_price = total_price / total_qty if total_qty else 0
        fc = prod_costs.get(prod_id, 0)
        margin = avg_price - fc
        result.append({
            "product_id": prod_id,
            "avg_price": round(avg_price, 2),
            "food_cost": round(fc, 2),
            "margin": round(margin, 2)
        })
    return result

@app.get("/riders/performance/", summary="Performance rider")
def rider_performance(db: Session = Depends(get_db)):
    """
    Statistiche per rider:
    - numero consegne effettuate
    - tempo medio consegna (da campo delivery_time)
    """
    riders = crud.get_riders(db, skip=0, limit=1000)
    orders = crud.get_orders(db, skip=0, limit=100000)
    perf_map = {}
    for rider in riders:
        deliveries = [o for o in orders if o.rider_id == rider.id]
        count = len(deliveries)
        avg_time = rider.delivery_time if rider.delivery_time is not None else 0
        perf_map[rider.id] = {
            "rider_id": rider.id,
            "name": rider.name,
            "avg_time": round(avg_time, 2),
            "deliveries": count
        }
    return list(perf_map.values())

# Fine file
