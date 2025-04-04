from typing import Optional
from models import Cart, Entree, Protein, Rice, Bean, Topping, Side, Drink
import uuid


def view_cart(cart: Cart) -> str:
    """Return a nicely formatted string representation of the current cart contents."""
    if not cart.entrees and not cart.sides and not cart.drinks:
        return "🛒 Your cart is empty."

    lines = ["🛒 Current cart:"]
    
    for idx, entree in enumerate(cart.entrees):
        lines.append(f"[{idx}] 🌯 Entree ({entree.type}) - ID: {entree.id}")
        if entree.protein:
            for p in entree.protein:
                lines.append(f"  🐓 Protein: {p.quantity}x {p.name}")
        if entree.rice:
            for r in entree.rice:
                lines.append(f"  🍚 Rice: {r.quantity}x {r.name}")
        if entree.beans:
            for b in entree.beans:
                lines.append(f"  🫘 Beans: {b.quantity}x {b.name}")
        if entree.toppings:
            for t in entree.toppings:
                lines.append(f"  🧅 Topping: {t.quantity}x {t.name}")
        lines.append(f"  🔢 Entree quantity: {entree.quantity}")
    
    for side in cart.sides:
        lines.append(f"🥑 Side: {side.quantity}x {side.name}")

    for drink in cart.drinks:
        lines.append(f"🥤 Drink: {drink.quantity}x {drink.size} {drink.name}")

    return "\n".join(lines)

def add_entree(cart: Cart, entree: Entree):
    """Add an entree to the cart."""
    entree.id = str(uuid.uuid4())
    cart.entrees.append(entree)
    print(f"Added new entree: {entree.type}")
    return cart

def remove_entree(cart: Cart, entree_id: str):
    """Remove an entree from the cart."""
    for entree in cart.entrees:
        if entree.id == entree_id:
            cart.entrees.remove(entree)
            print(f"Removed entree with ID {entree_id} from the cart.")
            return cart

    print(f"No entree found with ID {entree_id}. Nothing removed.")
    return cart

def edit_entree(cart: Cart, entree_id: str, updates: Entree) -> Optional[Cart]:
    """Edit fields of an existing entree in the cart, matching by ID."""
    for e in cart.entrees:
        if e.id == entree_id:
            if updates.type:
                e.type = updates.type
            if updates.protein:
                e.protein = updates.protein
            if updates.rice:
                e.rice = updates.rice
            if updates.beans:
                e.beans = updates.beans
            if updates.toppings:
                e.toppings = updates.toppings
            if updates.quantity:
                e.quantity = updates.quantity
            return cart
    
    print(f"No entree found with ID {entree_id}")
    return None

def add_side(cart: Cart, side: Side):
    """Add a side to the cart."""
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

# No function for editting drink size. I wonder if agent will delete and add new size drink.
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
