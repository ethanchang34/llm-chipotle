from models import Cart, Side, Drink
import cart_operations as ops

# Create a blank cart
cart = Cart(entree=[], drinks=[], sides=[])


# Test adding a drink ----------------------------------------
drink = Drink(name="Lemonade", size="Large", quantity=2)

ops.add_drink(cart, drink)

newDrink = Drink(name="Soda", size="Small")
ops.add_drink(cart, newDrink)

newerDrink = Drink(name="Soda", size="Small", quantity=3)
ops.add_drink(cart, newerDrink)

print("--- Cart contents ---")
for d in cart.drinks:
    print(f"- {d.quantity} {d.size} {d.name}")

# Test removing a drink ---------------------------------------
drink = Drink(name="Lemonade", size="Large", quantity=3)
ops.remove_drink(cart, drink)
ops.remove_drink(cart, drink)

newDrink = Drink(name="Soda", size="Small")
ops.remove_drink(cart, newDrink)

print("--- Cart contents ---")
for d in cart.drinks:
    print(f"- {d.quantity} {d.size} {d.name}")

# Test setting drink quantity ---------------------------------
drink = Drink(name="Soda", size="Small", quantity = 1)
ops.set_drink_quantity(cart, drink)

newDrink = Drink(name="Soda", size="Small", quantity = 0)
ops.set_drink_quantity(cart, newDrink)

print("--- Cart contents ---")
for d in cart.drinks:
    print(f"- {d.quantity} {d.size} {d.name}")

# Test adding sides -------------------------------------------
side = Side(name="Chips", quantity=2)
ops.add_side(cart, side)

newSide = Side(name="Chips & Guac", quantity=1)
ops.add_side(cart, newSide)

# Add more of an existing side
moreChips = Side(name="Chips", quantity=3)
ops.add_side(cart, moreChips)

print("--- Cart contents ---")
for s in cart.sides:
    print(f"- {s.quantity}x {s.name}")

# Test removing sides -----------------------------------------
side = Side(name="Chips", quantity=2)
ops.remove_side(cart, side)

side = Side(name="Chips & Guac", quantity=1)
ops.remove_side(cart, side)

print("--- Cart contents ---")
for s in cart.sides:
    print(f"- {s.quantity}x {s.name}")

# Test setting side quantity ----------------------------------
ops.set_side_quantity(cart, Side(name="Chips", quantity=2))
ops.set_side_quantity(cart, Side(name="Chips & Queso", quantity=4))

print("--- Cart contents ---")
for s in cart.sides:
    print(f"- {s.quantity}x {s.name}")
