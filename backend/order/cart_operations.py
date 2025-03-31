from typing import Optional
from models import Cart, OrderItem, IngredientWithQuantity, ProteinType, RiceType, BeanType, ToppingType, SideType, ExtraType, DrinkType
import uuid


def add_entree_to_cart(cart: Cart, entree_type: str, quantity: int = 1) -> int:
    """Add an empty entree to the cart. Other fields like protein/toppings can be set later."""
    entree = OrderItem(
        id=str(uuid.uuid4()),
        type=entree_type,
        quantity=quantity,
        protein=None,
        rice=None,
        beans=None,
        toppings=[],
        sides=[],
        extras=[],
        drinks=[],
    )
    cart.items.append(entree)
    return len(cart.items) - 1


def set_protein(cart: Cart, item_index: int, protein: ProteinType, quantity: int = 1):
    item = _get_item(cart, item_index)
    item.protein = IngredientWithQuantity(name=protein, quantity=quantity)


def set_rice(cart: Cart, item_index: int, rice: RiceType, quantity: int = 1):
    item = _get_item(cart, item_index)
    item.rice = IngredientWithQuantity(name=rice, quantity=quantity)


def set_beans(cart: Cart, item_index: int, beans: BeanType, quantity: int = 1):
    item = _get_item(cart, item_index)
    item.beans = IngredientWithQuantity(name=beans, quantity=quantity)


def add_topping(cart: Cart, item_index: int, topping: ToppingType, quantity: int = 1):
    item = _get_item(cart, item_index)
    _add_or_update(item.toppings, topping, quantity)


def add_side(cart: Cart, item_index: int, side: SideType, quantity: int = 1):
    item = _get_item(cart, item_index)
    _add_or_update(item.sides, side, quantity)


def add_extra(cart: Cart, item_index: int, extra: ExtraType, quantity: int = 1):
    item = _get_item(cart, item_index)
    _add_or_update(item.extras, extra, quantity)


def add_drink(cart: Cart, item_index: int, drink: DrinkType, quantity: int = 1):
    item = _get_item(cart, item_index)
    _add_or_update(item.drinks, drink, quantity)


def remove_item(cart: Cart, item_index: int):
    if 0 <= item_index < len(cart.items):
        cart.items.pop(item_index)


def _get_item(cart: Cart, index: int) -> OrderItem:
    if index < 0 or index >= len(cart.items):
        raise IndexError("Item index out of bounds")
    return cart.items[index]


def _add_or_update(ingredients_list: list, name: str, quantity: int):
    for item in ingredients_list:
        if item.name == name:
            item.quantity = quantity
            return
    ingredients_list.append(IngredientWithQuantity(name=name, quantity=quantity))
