from pydantic_ai import Agent, RunContext
from dataclasses import dataclass
import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@dataclass
class OrderDeps:
    cart: dict  # Replace with actual Cart class
    menu: dict  # Replace with actual Menu class

agent = Agent(
    model="gpt-3.5-turbo-0125",
    deps_type=OrderDeps,
    system_prompt="""
    You are a Chipotle ordering assistant. Guide the user in building their order. 
    You can view the menu, view the cart, add or modify items in the cart, etc.
    Use your tools when appropriate.
    """
)

@agent.tool
def view_menu(ctx: RunContext[OrderDeps]) -> dict:
    return ctx.deps.menu

@agent.tool
def add_item_to_cart(ctx: RunContext[OrderDeps], item_type: str, menu_item_id: str) -> str:
    # Dummy implementation
    ctx.deps.cart.setdefault("items", []).append({"type": item_type, "id": menu_item_id})
    return f"Added {item_type} to the cart."

# You can keep adding more tools like `remove_item`, `set_protein`, etc.
