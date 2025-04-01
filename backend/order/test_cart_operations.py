from models import Cart, Entree, Protein, Rice, Bean, Topping, Side, Drink
import cart_operations as ops

# Create a blank cart
cart = Cart(entree=[], drinks=[], sides=[])


# Test adding a drink ----------------------------------------
print("[TEST] Add drink")
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
print("[TEST] Remove drink")
drink = Drink(name="Lemonade", size="Large", quantity=3)
ops.remove_drink(cart, drink)
ops.remove_drink(cart, drink)

newDrink = Drink(name="Soda", size="Small")
ops.remove_drink(cart, newDrink)

print("--- Cart contents ---")
for d in cart.drinks:
    print(f"- {d.quantity} {d.size} {d.name}")

# Test setting drink quantity ---------------------------------
print("[TEST] Set drink quantity")
drink = Drink(name="Soda", size="Small", quantity = 1)
ops.set_drink_quantity(cart, drink)

newDrink = Drink(name="Soda", size="Small", quantity = 0)
ops.set_drink_quantity(cart, newDrink)

print("--- Cart contents ---")
for d in cart.drinks:
    print(f"- {d.quantity} {d.size} {d.name}")

# Test adding sides -------------------------------------------
print("[TEST] Add side")
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
print("[TEST] Remove side")
side = Side(name="Chips", quantity=2)
ops.remove_side(cart, side)

side = Side(name="Chips & Guac", quantity=1)
ops.remove_side(cart, side)

print("--- Cart contents ---")
for s in cart.sides:
    print(f"- {s.quantity}x {s.name}")

# Test setting side quantity ----------------------------------
print("[TEST] Set side quantity")
ops.set_side_quantity(cart, Side(name="Chips", quantity=2))
ops.set_side_quantity(cart, Side(name="Chips & Queso", quantity=4))

print("--- Cart contents ---")
for s in cart.sides:
    print(f"- {s.quantity}x {s.name}")

# Test adding an entree ---------------------------------------
print("[TEST] Add entree")
entree1 = Entree(
    id="1",
    type="Bowl",
    protein=[Protein(name="Chicken", quantity=1)],
    rice=[Rice(name="White", quantity=1)],
    beans=[Bean(name="Pinto", quantity=1)],
    toppings=[
        Topping(name="Lettuce"),
        Topping(name="Cheese")
    ],
    quantity=1
)
ops.add_entree(cart, entree1)

entree2 = Entree(
    id="2",
    type="Burrito",
    protein=[Protein(name="Steak", quantity=1)],
    rice=[Rice(name="Brown", quantity=1)],
    quantity=1
)
ops.add_entree(cart, entree2)

print("Final cart contents:")
for i, e in enumerate(cart.entrees):
    print(f"Entree #{i+1}:")
    print(f"  ID: {e.id}")
    print(f"  Type: {e.type}")
    print(f"  Quantity: {e.quantity}")
    print(f"  Protein: {[f'{p.name} x{p.quantity}' for p in e.protein]}")
    print(f"  Rice: {[f'{r.name} x{r.quantity}' for r in e.rice]}")
    print(f"  Beans: {[f'{b.name} x{b.quantity}' for b in e.beans]}")
    print(f"  Toppings: {[f'{t.name} x{t.quantity}' for t in e.toppings]}")