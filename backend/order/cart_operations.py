from typing import Dict
from models import Cart, Menu, MenuItem, OrderItem

def add_item_to_cart(cart: Cart, item: OrderItem) -> None:
    """Adds an OrderItem to the cart."""
    cart.items.append(item)

def remove_item_from_cart(cart: Cart, index: int) -> None:
    """Removes an item from the cart by index."""
    if index < 0 or index >= len(cart.items):
        raise IndexError(f"Invalid index {index}.")
    cart.items.pop(index)

def update_item_quantity(cart: Cart, index: int, new_quantity: int) -> None:
    """Updates the quantity of an item."""
    if index < 0 or index >= len(cart.items):
        raise IndexError(f"Invalid index {index}.")
    cart.items[index].quantity = new_quantity
