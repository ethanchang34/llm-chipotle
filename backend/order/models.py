from typing import List, Optional, Literal
from pydantic import BaseModel

ProteinType = Literal["Chicken", "Steak", "Barbacoa", "Carnitas", "Sofritas", "Veggie"]
RiceType = Literal["White", "Brown", "None"]
BeanType = Literal["Blank", "Pinto", "None"]
ToppingType = Literal["Lettuce", "Fajita Veggies", "Mild Salsa", "Medium Salsa", "Hot Salsa", "Corn Salsa", "Cheese", "Sour Cream", "Guacamole"]
SideType = Literal["Chips", "Chips & Guac", "Chips & Queso"]
DrinkType = Literal["Water", "Lemonade", "Soda"]
Size = Literal["Small", "Medium", "Large"]

class Topping(BaseModel):
    name: ToppingType
    quantity: Optional[int] = 1  # How many scoops/servings of this topping

class SideItem(BaseModel):
    name: SideType
    quantity: Optional[int] = 1

class Drink(BaseModel):
    name: DrinkType
    size: Optional[Size] = "Medium"
    quantity: Optional[int] = 1

class OrderItem(BaseModel):
    id: str
    type: str  # "Bowl", "Burrito", etc.
    protein: ProteinType
    protein_quantity: Optional[int] = 1 
    rice: Optional[RiceType] = None
    rice_quantity: Optional[int] = 1
    beans: Optional[BeanType] = None
    beans_quantity: Optional[int] = 1
    toppings: Optional[List[ToppingType]] = []
    sides: Optional[List[SideType]] = []
    drinks: Optional[List[DrinkType]] = []
    quantity: int = 1

class Cart(BaseModel):
    items: List[OrderItem]
