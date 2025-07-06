# app/main.py
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from io import StringIO
import csv
from datetime import datetime
from collections import defaultdict
from . import models, schemas, crud
from .database import SessionLocal, engine

# Create database tables
target_metadata = models.Base.metadata
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Food Cost Dashboard API", version="0.1")

# CORS configuration
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---- CRUD Endpoints ----

# Ingredients
@app.post("/ingredients/", response_model=schemas.Ingredient)
def create_ingredient(ingredient: schemas.IngredientCreate, db: Session = Depends(get_db)):
    return crud.create_ingredient(db, ingredient)

@app.get("/ingredients/", response_model=list[schemas.Ingredient])
def read_ingredients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_ingredients(db, skip=skip, limit=limit)

@app.get("/ingredients/{ingredient_id}", response_model=schemas.Ingredient)
def read_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    db_ing = crud.get_ingredient(db, ingredient_id)
    if not db_ing:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return db_ing

@app.put("/ingredients/{ingredient_id}", response_model=schemas.Ingredient)
def update_ingredient(ingredient_id: int, ingredient: schemas.IngredientCreate, db: Session = Depends(get_db)):
    db_ing = crud.update_ingredient(db, ingredient_id, ingredient)
    if not db_ing:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return db_ing

@app.delete("/ingredients/{ingredient_id}", status_code=204)
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    crud.delete_ingredient(db, ingredient_id)
    return

# Products
@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@app.get("/products/", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_products(db, skip=skip, limit=limit)

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_prod = crud.get_product(db, product_id)
    if not db_prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_prod

@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_prod = crud.update_product(db, product_id, product)
    if not db_prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_prod

@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    crud.delete_product(db, product_id)
    return

# Recipes
@app.post("/recipes/", response_model=schemas.Recipe)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    return crud.create_recipe(db, recipe)

@app.get("/recipes/", response_model=list[schemas.Recipe])
def read_recipes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_recipes(db, skip=skip, limit=limit)

@app.delete("/recipes/{recipe_id}", status_code=204)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    crud.delete_recipe(db, recipe_id)
    return

# Orders
@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order)

@app.get("/orders/", response_model=list[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_orders(db, skip=skip, limit=limit)

@app.get("/orders/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_ord = crud.get_order(db, order_id)
    if not db_ord:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_ord

@app.delete("/orders/{order_id}", status_code=204)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    crud.delete_order(db, order_id)
    return

# Inventory Movements
@app.post("/inventory/", response_model=schemas.InventoryMovement)
def create_inventory_movement(mov: schemas.InventoryMovementCreate, db: Session = Depends(get_db)):
    return crud.create_inventory_movement(db, mov)

@app.get("/inventory/", response_model=list[schemas.InventoryMovement])
def read_inventory_movements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_inventory_movements(db, skip=skip, limit=limit)

@app.delete("/inventory/{movement_id}", status_code=204)
def delete_inventory_movement(movement_id: int, db: Session = Depends(get_db)):
    crud.delete_inventory_movement(db, movement_id)
    return

# Riders
@app.post("/riders/", response_model=schemas.Rider)
def create_rider(rider: schemas.RiderCreate, db: Session = Depends(get_db)):
    return crud.create_rider(db, rider)

@app.get("/riders/", response_model=list[schemas.Rider])
def read_riders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_riders(db, skip=skip, limit=limit)

@app.get("/riders/{rider_id}", response_model=schemas.Rider)
def read_rider(rider_id: int, db: Session = Depends(get_db)):
    db_r = crud.get_rider(db, rider_id)
    if not db_r:
        raise HTTPException(status_code=404, detail="Rider not found")
    return db_r

@app.put("/riders/{rider_id}", response_model=schemas.Rider)
def update_rider(rider_id: int, rider: schemas.RiderCreate, db: Session = Depends(get_db)):
    db_r = crud.update_rider(db, rider_id, rider)
    if not db_r:
        raise HTTPException(status_code=404, detail="Rider not found")
    return db_r

@app.delete("/riders/{rider_id}", status_code=204)
def delete_rider(rider_id: int, db: Session = Depends(get_db)):
    crud.delete_rider(db, rider_id)
    return

# ---- CSV Import Endpoints ----

# Orders import
@app.post("/orders/import-csv/", response_model=list[schemas.Order])
async def import_orders_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    content = await file.read()
    text = content.decode('utf-8')
    reader = csv.DictReader(StringIO(text))
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

# Ingredients import
@app.post("/ingredients/import-costs-csv/", response_model=list[schemas.Ingredient])
async def import_ingredient_costs_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    content = await file.read()
    text = content.decode('utf-8')
    reader = csv.DictReader(StringIO(text))
    results = []
    for row in reader:
        ing = None
        if row.get('id'):
            ing = crud.get_ingredient(db, int(row['id']))
        else:
            ing = db.query(models.Ingredient).filter(models.Ingredient.name == row['name']).first()
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

# Products import
@app.post("/products/import-csv/", response_model=list[schemas.Product])
async def import_products_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    content = await file.read()
    text = content.decode('utf-8')
    reader = csv.DictReader(StringIO(text))
    created = []
    for row in reader:
        prod_in = schemas.ProductCreate(name=row['name'])
        obj = crud.create_product(db, prod_in)
        created.append(obj)
    return created

# Recipes import
@app.post("/recipes/import-csv/", response_model=list[schemas.Recipe])
async def import_recipes_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    content = await file.read()
    text = content.decode('utf-8')
    reader = csv.DictReader(StringIO(text))
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

# Inventory import
@app.post("/inventory/import-csv/", response_model=list[schemas.InventoryMovement])
async def import_inventory_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    content = await file.read()
    text = content.decode('utf-8')
    reader = csv.DictReader(StringIO(text))
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

# Riders import
@app.post("/riders/import-csv/", response_model=list[schemas.Rider])
async def import_riders_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    content = await file.read()
    text = content.decode('utf-8')
    reader = csv.DictReader(StringIO(text))
    created = []
    for row in reader:
        rider_in = schemas.RiderCreate(
            name=row['name'],
            delivery_time=float(row['delivery_time']) if row.get('delivery_time') else None
        )
        obj = crud.create_rider(db, rider_in)
        created.append(obj)
    return created

# ---- Food Cost endpoint ----
@app.get(
    "/products/food-cost/",
    response_model=list[schemas.ProductFoodCost],
    summary="Food cost per prodotto"
)
def read_food_costs(db: Session = Depends(get_db)):
    recipes = crud.get_all_recipes(db)
    ingredients = crud.get_ingredients(db, skip=0, limit=1000)
    cost_map = {ing.id: ing.unit_cost for ing in ingredients}
    prod_costs = defaultdict(float)
    for r in recipes:
        prod_costs[r.product_id] += cost_map.get(r.ingredient_id, 0) * r.quantity
    return [{"product_id": pid, "food_cost": round(cost, 2)} for pid, cost in prod_costs.items()]



@app.get(
    "/products/margine-lordo/",
    response_model=list[schemas.ProductMargin],
    summary="Margine lordo per prodotto"
)
def read_product_margin(db: Session = Depends(get_db)):
    # 1) Aggrega ordini per prodotto
    stats = db.query(
        models.Order.product_id,
        func.sum(models.Order.price).label("total_price"),
        func.sum(models.Order.quantity).label("total_qty")
    ).group_by(models.Order.product_id).all()

    # 2) Calcola food cost per prodotto
    ingredients = crud.get_ingredients(db, skip=0, limit=1000)
    recipes = crud.get_all_recipes(db, skip=0, limit=1000)
    cost_map = {ing.id: ing.unit_cost for ing in ingredients}
    prod_costs = defaultdict(float)
    for r in recipes:
        prod_costs[r.product_id] += cost_map.get(r.ingredient_id, 0) * r.quantity

    # 3) Componi la risposta con avg_price, food_cost e margine
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
