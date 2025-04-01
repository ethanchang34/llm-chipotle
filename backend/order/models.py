from typing import List, Literal
from pydantic import BaseModel

OrderType = Literal["Bowl", "Burrito", "Tacos", "Salad", "Quesadilla"]

class Protein(BaseModel):
    name: Literal["Chicken", "Steak", "Barbacoa", "Carnitas", "Sofritas", "Veggie"]
    quantity: int = 1

class Rice(BaseModel):
    name: Literal["White", "Brown", "None"]
    quantity: int = 1

class Bean(BaseModel):
    name: Literal["Blank", "Pinto", "None"]
    quantity: int = 1

class Topping(BaseModel):
    name: Literal["Lettuce", "Fajita Veggies", "Mild Salsa", "Medium Salsa", "Hot Salsa", "Corn Salsa", "Cheese", "Sour Cream", "Guacamole"]
    quantity: int = 1

class Side(BaseModel):
    name: Literal["Chips", "Chips & Guac", "Chips & Queso"]
    quantity: int = 1

class Drink(BaseModel):
    name: Literal["Water", "Lemonade", "Soda"]
    size: Literal["Small", "Medium", "Large"] = "Medium"
    quantity: int = 1

class Entree(BaseModel):
    id: str
    type: OrderType
    protein: List[Protein] = []
    rice: List[Rice] = []
    beans: List[Bean] = []
    toppings: List[Topping] = []
    quantity: int = 1

class Cart(BaseModel):
    entrees: List[Entree] = []
    sides: List[Side] = []
    drinks: List[Drink] = []

