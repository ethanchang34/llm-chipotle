from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
from order.models import Cart, Drink
from order.cart_operations import add_drink
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@dataclass
class CartDeps:
    cart: Cart


agent = Agent(
    model="gpt-3.5-turbo-0125",
    deps_type=CartDeps,
    system_prompt="""
    You are a Chipotle ordering assistant. Guide the user in building their order. 
    You can add or modify items in the cart, etc.
    Use your tools when appropriate.
    To edit or remove an entree, use view_cart to get the correct entree ID.
    """
)

@agent.tool
def add_drink_to_cart(ctx: RunContext[CartDeps], name: str, size: str = "Medium", quantity: int = 1) -> str:
    """Add a drink to the user's cart."""
    try:
        add_drink(ctx.deps.cart, name=name, size=size, quantity=quantity)
        return f"✅ Added {quantity} {size} {name}(s) to your cart."
    except ValueError as e:
        return f"❌ {str(e)}"