TOOLS = {}
def tool(name):
    def deco(fn):
        TOOLS[name] = fn
        return fn
    return deco

def call_tool(name: str, **kwargs):
    if name not in TOOLS:
        raise ValueError(f"Unknown tool: {name}")
    return TOOLS[name](**kwargs)