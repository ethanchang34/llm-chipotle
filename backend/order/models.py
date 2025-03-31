from typing import List, Optional, Union
from pydantic import BaseModel

class Topping(BaseModel):
    name: str  # e.g., "Cheese", "Sour Cream"
    quantity: Optional[int] = 1  # How many scoops/servings of this topping

class SideItem(BaseModel):
    name: str  # e.g., "Chips", "Chips & Guac"
    quantity: Optional[int] = 1

class Drink(BaseModel):
    name: str  # e.g., "Coke", "Lemonade"
    size: Optional[str] = "Medium"
    quantity: Optional[int] = 1

class OrderItem(BaseModel):
    id: str
    type: str  # "Bowl", "Burrito", etc.
    protein: str
    protein_quantity: Optional[int] = 1 
    rice: Optional[str] = None
    rice_quantity: Optional[int] = 1
    beans: Optional[str] = None
    beans_quantity: Optional[int] = 1
    toppings: Optional[List[Topping]] = []
    sides: Optional[List[SideItem]] = []
    drinks: Optional[List[Drink]] = []
    quantity: int  # quantity of the entree item

class Cart(BaseModel):
    items: List[OrderItem]
