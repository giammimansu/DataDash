from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# -----------------
# Ingredient
# -----------------
class IngredientBase(BaseModel):
    name: str
    unit_cost: float

class IngredientCreate(IngredientBase):
    pass

class Ingredient(IngredientBase):
    id: int

    class Config:
        from_attributes = True

# -----------------
# Product
# -----------------
class ProductBase(BaseModel):
    name: str

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True

# -----------------
# Recipe
# -----------------
class RecipeBase(BaseModel):
    product_id: int
    ingredient_id: int
    quantity: float

class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int

    class Config:
        from_attributes = True

# -----------------
# Order
# -----------------
class OrderBase(BaseModel):
    timestamp: Optional[datetime] = None
    product_id: int
    quantity: int
    rider_id: Optional[int] = None
    price: float

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int

    class Config:
        from_attributes = True

# -----------------
# InventoryMovement
# -----------------
class InventoryMovementBase(BaseModel):
    ingredient_id: int
    quantity: float
    movement_type: str
    timestamp: Optional[datetime] = None

class InventoryMovementCreate(InventoryMovementBase):
    pass

class InventoryMovement(InventoryMovementBase):
    id: int

    class Config:
        from_attributes = True

# -----------------
# Rider
# -----------------
class RiderBase(BaseModel):
    name: str
    delivery_time: Optional[float]

class RiderCreate(RiderBase):
    pass

class Rider(RiderBase):
    id: int

    class Config:
        from_attributes = True




class ProductFoodCost(BaseModel):
    product_id: int
    food_cost: float

    class Config:
        from_attributes = True

class ProductMargin(BaseModel):
    product_id: int
    avg_price: float
    food_cost: float
    margin: float

    class Config:
        from_attributes = True
