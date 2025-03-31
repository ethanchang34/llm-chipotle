from typing import List, Optional, Literal
from pydantic import BaseModel

OrderType = Literal["Bowl", "Burrito", "Tacos", "Salad", "Quesadilla"]
ProteinType = Literal["Chicken", "Steak", "Barbacoa", "Carnitas", "Sofritas", "Veggie"]
RiceType = Literal["White", "Brown", "None"]
BeanType = Literal["Blank", "Pinto", "None"]

class Topping(BaseModel):
    name: Literal["Lettuce", "Fajita Veggies", "Mild Salsa", "Medium Salsa", "Hot Salsa", "Corn Salsa", "Cheese", "Sour Cream", "Guacamole"]
    quantity: Optional[int] = 1

class SideItem(BaseModel):
    name: Literal["Chips", "Chips & Guac", "Chips & Queso"]
    quantity: Optional[int] = 1

class Drink(BaseModel):
    name: Literal["Water", "Lemonade", "Soda"]
    size: Literal["Small", "Medium", "Large"]
    quantity: Optional[int] = 1

class OrderItem(BaseModel):
    id: str
    type: OrderType
    protein: ProteinType
    protein_quantity: Optional[int] = 1 
    rice: Optional[RiceType] = None
    rice_quantity: Optional[int] = 1
    beans: Optional[BeanType] = None
    beans_quantity: Optional[int] = 1
    toppings: Optional[List[Topping]] = []
    sides: Optional[List[SideItem]] = []
    drinks: Optional[List[Drink]] = []
    quantity: int = 1

class Cart(BaseModel):
    items: List[OrderItem]
