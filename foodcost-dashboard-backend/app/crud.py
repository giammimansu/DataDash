from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime
from typing import Optional, List


# -----------------
# INGREDIENT CRUD
# -----------------
def create_ingredient(db: Session, ingredient: schemas.IngredientCreate):
    db_ingredient = models.Ingredient(**ingredient.dict())
    db.add(db_ingredient)
    db.commit()
    db.refresh(db_ingredient)
    return db_ingredient

def get_ingredient(db: Session, ingredient_id: int):
    return db.query(models.Ingredient).filter(models.Ingredient.id == ingredient_id).first()

def get_ingredients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ingredient).offset(skip).limit(limit).all()

def delete_ingredient(db: Session, ingredient_id: int):
    obj = db.query(models.Ingredient).get(ingredient_id)
    if obj:
        db.delete(obj)
        db.commit()

def update_ingredient(db: Session, ingredient_id: int, ingredient: schemas.IngredientCreate):
    obj = db.query(models.Ingredient).get(ingredient_id)
    if obj:
        obj.name = ingredient.name
        obj.unit_cost = ingredient.unit_cost
        db.commit()
        db.refresh(obj)
    return obj

# -----------------
# PRODUCT CRUD
# -----------------
def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def delete_product(db: Session, product_id: int):
    obj = db.query(models.Product).get(product_id)
    if obj:
        db.delete(obj)
        db.commit()

def update_product(db: Session, product_id: int, product: schemas.ProductCreate):
    obj = db.query(models.Product).get(product_id)
    if obj:
        obj.name = product.name
        db.commit()
        db.refresh(obj)
    return obj

# -----------------
# RECIPE CRUD
# -----------------
def create_recipe(db: Session, recipe: schemas.RecipeCreate):
    db_recipe = models.Recipe(**recipe.dict())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def get_recipes_by_product(db: Session, product_id: int):
    return db.query(models.Recipe).filter(models.Recipe.product_id == product_id).all()

def delete_recipe(db: Session, recipe_id: int):
    obj = db.query(models.Recipe).get(recipe_id)
    if obj:
        db.delete(obj)
        db.commit()

# -----------------
# ORDER CRUD
# -----------------
def create_order(db: Session, order: schemas.OrderCreate):
    data = order.dict()
    if data.get("timestamp") is None:
        data["timestamp"] = datetime.utcnow()
    db_order = models.Order(**data)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()

def delete_order(db: Session, order_id: int):
    obj = db.query(models.Order).get(order_id)
    if obj:
        db.delete(obj)
        db.commit()

# -----------------
# INVENTORY MOVEMENT CRUD
# -----------------
def create_inventory_movement(db: Session, movement: schemas.InventoryMovementCreate):
    data = movement.dict()
    if data.get("timestamp") is None:
        data["timestamp"] = datetime.utcnow()
    db_movement = models.InventoryMovement(**data)
    db.add(db_movement)
    db.commit()
    db.refresh(db_movement)
    return db_movement

def get_inventory_movements(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.InventoryMovement).offset(skip).limit(limit).all()

def delete_inventory_movement(db: Session, movement_id: int):
    obj = db.query(models.InventoryMovement).get(movement_id)
    if obj:
        db.delete(obj)
        db.commit()

# -----------------
# RIDER CRUD
# -----------------
def create_rider(db: Session, rider: schemas.RiderCreate):
    db_rider = models.Rider(**rider.dict())
    db.add(db_rider)
    db.commit()
    db.refresh(db_rider)
    return db_rider

def get_rider(db: Session, rider_id: int):
    return db.query(models.Rider).filter(models.Rider.id == rider_id).first()

def get_riders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Rider).offset(skip).limit(limit).all()

def delete_rider(db: Session, rider_id: int):
    obj = db.query(models.Rider).get(rider_id)
    if obj:
        db.delete(obj)
        db.commit()

def update_rider(db: Session, rider_id: int, rider: schemas.RiderCreate):
    obj = db.query(models.Rider).get(rider_id)
    if obj:
        obj.name = rider.name
        obj.delivery_time = rider.delivery_time
        db.commit()
        db.refresh(obj)
    return obj



# --- Ordini filtrati ---
def get_orders_filtered(
    db: Session,
    date_from: Optional[datetime] = None,
    date_to:   Optional[datetime] = None,
    product_id: Optional[int] = None,
    rider_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100
) -> List[models.Order]:
    query = db.query(models.Order)
    if date_from:
        query = query.filter(models.Order.timestamp >= date_from)
    if date_to:
        query = query.filter(models.Order.timestamp <= date_to)
    if product_id is not None:
        query = query.filter(models.Order.product_id == product_id)
    if rider_id is not None:
        query = query.filter(models.Order.rider_id == rider_id)
    return query.order_by(models.Order.timestamp).offset(skip).limit(limit).all()

# --- Ingredienti filtrati ---
def get_ingredients_filtered(
    db: Session,
    name_contains: Optional[str] = None,
    cost_min: Optional[float] = None,
    cost_max: Optional[float] = None,
    skip: int = 0,
    limit: int = 100
) -> List[models.Ingredient]:
    query = db.query(models.Ingredient)
    if name_contains:
        query = query.filter(models.Ingredient.name.ilike(f"%{name_contains}%"))
    if cost_min is not None:
        query = query.filter(models.Ingredient.unit_cost >= cost_min)
    if cost_max is not None:
        query = query.filter(models.Ingredient.unit_cost <= cost_max)
    return query.order_by(models.Ingredient.name).offset(skip).limit(limit).all()



# Recupera tutte le ricette
def get_all_recipes(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.Recipe).offset(skip).limit(limit).all()
