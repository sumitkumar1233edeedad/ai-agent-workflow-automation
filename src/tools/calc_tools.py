from .registry import tool

@tool("calculator")
def calculator(expr: str, **_) -> float:
    return eval(expr, {"__builtins__": {}}, {})