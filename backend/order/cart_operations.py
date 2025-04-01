from typing import Optional
from models import Cart, Side, Drink
import uuid

# Add entree to cart
# Add side to cart

def add_side(cart: Cart, side: Side):
    """Add a side to the cart"""
    for s in cart.sides:
        if s.name == side.name:
            s.quantity += side.quantity
            break
    else:
        cart.sides.append(side)
    print(f"Added '{side.name}' (x{side.quantity}) to cart.")
    return cart

def remove_side(cart: Cart, side: Side):
    """Remove a side from the cart."""
    for s in cart.sides:
        if s.name == side.name:
            s.quantity -= side.quantity
            if s.quantity <= 0:
                cart.sides.remove(s)
                print(f"Removed side '{side.name}' from cart.")
            else:
                print(f"Decreased quantity of side '{side.name}' by {side.quantity}")
            break
    else:
        print(f"Side '{side.name}' ({side.size}) not found in cart.")
    return cart

def set_side_quantity(cart: Cart, side: Side):
    """Set the quantity of a specific side in the cart."""
    for s in cart.sides:
        if s.name == side.name:
            if side.quantity <= 0:
                cart.sides.remove(s)
                print(f"Removed side '{side.name}' from cart.")
            else:
                s.quantity = side.quantity
                print(f"Set quantity of side '{side.name}' to {side.quantity}")
            return cart

    if side.quantity > 0:
        add_side(cart, side)

    return cart

def add_drink(cart: Cart, drink: Drink):
    """Add a drink to the cart"""
    for d in cart.drinks:
        if d.name == drink.name and d.size == drink.size:
            d.quantity += drink.quantity
            break
    else:
        cart.drinks.append(drink)
    print(f"Added {drink.quantity} {drink.size} {drink.name}(s) to the cart.")
    return cart

def remove_drink(cart: Cart, drink: Drink):
    """Remove a drink from the cart"""
    for d in cart.drinks:
        if d.name == drink.name and d.size == d.size:
            d.quantity -= drink.quantity
            if d.quantity <= 0:
                cart.drinks.remove(d)
                print(f"Removed drink '{d.name}' ({d.size}) from cart.")
            else:
                print(f"Decreased quantity of '{d.name}' ({d.size}) to {d.quantity}.")
            break
    else:
        print(f"Drink '{drink.name}' ({drink.size}) not found in cart.")
    return cart

def set_drink_quantity(cart: Cart, drink: Drink):
    """Set the quantity of a specific drink in the cart."""
    for d in cart.drinks:
        if d.name == drink.name and d.size == drink.size:
            if drink.quantity <= 0:
                cart.drinks.remove(d)
                print(f"Removed drink '{drink.name}' ({drink.size}) from cart.")
            else:
                d.quantity = drink.quantity
                print(f"Set quantity of drink '{drink.name}' ({drink.size}) to {drink.quantity}.")
            return cart

    if drink.quantity > 0:
        add_drink(cart, drink)

    return cart

# -------------temp non-functional functinos below --------------
# def add_entree_to_cart(cart: Cart, entree_type: str, quantity: int = 1) -> int:
#     """Add an empty entree to the cart. Other fields like protein/toppings can be set later."""
#     entree = OrderItem(
#         id=str(uuid.uuid4()),
#         type=entree_type,
#         quantity=quantity,
#         protein=None,
#         rice=None,
#         beans=None,
#         toppings=[],
#         sides=[],
#         extras=[],
#         drinks=[],
#     )
#     cart.items.append(entree)
#     return len(cart.items) - 1


# def set_protein(cart: Cart, item_index: int, protein: ProteinType, quantity: int = 1):
#     item = _get_item(cart, item_index)
#     item.protein = IngredientWithQuantity(name=protein, quantity=quantity)


# def set_rice(cart: Cart, item_index: int, rice: RiceType, quantity: int = 1):
#     item = _get_item(cart, item_index)
#     item.rice = IngredientWithQuantity(name=rice, quantity=quantity)


# def set_beans(cart: Cart, item_index: int, beans: BeanType, quantity: int = 1):
#     item = _get_item(cart, item_index)
#     item.beans = IngredientWithQuantity(name=beans, quantity=quantity)


# def add_topping(cart: Cart, item_index: int, topping: ToppingType, quantity: int = 1):
#     item = _get_item(cart, item_index)
#     _add_or_update(item.toppings, topping, quantity)


# def add_side(cart: Cart, item_index: int, side: SideType, quantity: int = 1):
#     item = _get_item(cart, item_index)
#     _add_or_update(item.sides, side, quantity)



# def remove_item(cart: Cart, item_index: int):
#     if 0 <= item_index < len(cart.items):
#         cart.items.pop(item_index)


# def _get_item(cart: Cart, index: int) -> OrderItem:
#     if index < 0 or index >= len(cart.items):
#         raise IndexError("Item index out of bounds")
#     return cart.items[index]


# def _add_or_update(ingredients_list: list, name: str, quantity: int):
#     for item in ingredients_list:
#         if item.name == name:
#             item.quantity = quantity
#             return
#     ingredients_list.append(IngredientWithQuantity(name=name, quantity=quantity))
