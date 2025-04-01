from models import Cart, Drink
from cart_operations import add_drink, remove_drink, set_drink_quantity

# Create a blank cart
cart = Cart(entree=[], drinks=[], sides=[])


# Test adding a drink ----------------------------------------
drink = Drink(name="Lemonade", size="Large", quantity=2)

add_drink(cart, drink)

newDrink = Drink(name="Soda", size="Small")
add_drink(cart, newDrink)

newerDrink = Drink(name="Soda", size="Small", quantity=3)
add_drink(cart, newerDrink)

print("--- Cart contents ---")
for d in cart.drinks:
    print(f"- {d.quantity} {d.size} {d.name}")

# Test removing a drink ---------------------------------------
drink = Drink(name="Lemonade", size="Large", quantity=3)
remove_drink(cart, drink)
remove_drink(cart, drink)

newDrink = Drink(name="Soda", size="Small")
remove_drink(cart, newDrink)

print("--- Cart contents ---")
for d in cart.drinks:
    print(f"- {d.quantity} {d.size} {d.name}")

# Test setting drink quantity ---------------------------------
drink = Drink(name="Soda", size="Small", quantity = 1)
set_drink_quantity(cart, drink)

newDrink = Drink(name="Soda", size="Small", quantity = 0)
set_drink_quantity(cart, newDrink)

print("--- Cart contents ---")
for d in cart.drinks:
    print(f"- {d.quantity} {d.size} {d.name}")