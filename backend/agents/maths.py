# Required imports
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from backend.agents.openai_client import get_openai_client


# Basic math tools using @tool decorator
@tool
def add(a: float, b: float) -> float:
    """Returns the sum of two numbers."""
    return a + b


@tool
def subtract(a: float, b: float) -> float:
    """Returns the difference of two numbers."""
    return a - b


@tool
def multiply(a: float, b: float) -> float:
    """Returns the product of two numbers."""
    return a * b


@tool
def divide(a: float, b: float) -> float:
    """Returns the division of two numbers. If b is 0, returns 'Error: division by zero'."""
    if b == 0:
        return "Error: division by zero"
    return a / b


# List of tools
tools = [add, subtract, multiply, divide]

# LLM initialization (you can change the model to the one you have configured)
llm = get_openai_client()

# ReAct agent initialization using create_react_agent
maths_agent = create_react_agent(
    llm, tools, prompt="You are a helpful math assistant.", name="maths_agent"
)
