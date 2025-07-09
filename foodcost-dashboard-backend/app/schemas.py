from pydantic import BaseModel, EmailStr, Field , validator 
import re
from typing import Optional, List
from datetime import datetime

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(
        ...,
        min_length=8,
        description="Minimo 8 caratteri, con almeno una maiuscola, una minuscola, un numero e un carattere speciale"
    )

    @validator('password')
    def password_complexity(cls, v):
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&]).+$'
        if not re.match(pattern, v):
            raise ValueError(
                'La password deve contenere almeno: una lettera maiuscola, una minuscola, un numero e un carattere speciale'
            )
        return v

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserInDB(BaseModel):
    id: int
    email: EmailStr
    class Config:
        orm_mode = True

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
        orm_mode = True

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
        orm_mode = True

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
        orm_mode = True

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
        orm_mode = True

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
        orm_mode = True

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
        orm_mode = True

# -----------------
# Dashboard DTOs
# -----------------
class ProductFoodCost(BaseModel):
    product_id: int
    food_cost: float
    class Config:
        orm_mode = True

class ProductMargin(BaseModel):
    product_id: int
    avg_price: float
    food_cost: float
    margin: float
    class Config:
        orm_mode = True
