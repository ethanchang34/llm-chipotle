from pydantic_ai import Agent, RunContext
from order.models import Cart, Menu, OrderItem
from order import cart_operations as ops
from dataclasses import dataclass

@dataclass
class OrderAgentDeps:
    cart: Cart
    menu: Menu

order_agent = Agent(
    model="openai:gpt-3.5-turbo",  # or whichever model you're using
    deps_type=OrderAgentDeps,
    system_prompt="""
    You are a Chipotle ordering assistant. You help users add or remove items from their cart using the tools provided.
    Use the available menu options to assist them with building an accurate order.
    """
)

@order_agent.tool
def view_cart(ctx: RunContext[OrderAgentDeps]) -> Cart:
    """Returns the current cart."""
    return ctx.deps.cart

@order_agent.tool
def add_item(ctx: RunContext[OrderAgentDeps], item: OrderItem) -> str:
    """Add a new item to the cart."""
    index = ops.add_item_to_cart(ctx.deps.cart, ctx.deps.menu, item)
    return f"Added {item.type} to cart at index {index}."

@order_agent.tool
def remove_item(ctx: RunContext[OrderAgentDeps], index: int) -> str:
    """Remove an item from the cart."""
    ops.remove_item_from_cart(ctx.deps.cart, index)
    return f"Removed item at index {index} from cart."

@order_agent.tool
def update_quantity(ctx: RunContext[OrderAgentDeps], index: int, quantity: int) -> str:
    """Update quantity of an item in the cart."""
    ops.update_item_quantity(ctx.deps.cart, index, quantity)
    return f"Updated quantity of item at index {index} to {quantity}."
