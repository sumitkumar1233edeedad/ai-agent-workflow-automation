from langgraph.graph import StateGraph, END
from .models import AgentState
from .workflows.handlers import HANDLERS


def build_graph():
    g = StateGraph(AgentState)

    def router(state: AgentState):
        wid = state.selected_workflow
        if wid not in HANDLERS:
            return "unsupported"
        return "run"

    def run_workflow(state: AgentState):
        handler = HANDLERS[state.selected_workflow]
        final_out = None
        step_res = []
        err = None
        try:
            final_out, step_res = handler(state.user_request)
        except Exception as e:
            err = str(e)
        return {
            "final_output": final_out,
            "step_results": step_res,
            "error": err,
        }

    def unsupported(state: AgentState):
        return {
            "final_output": None,
            "step_results": [],
            "error": f"No handler for {state.selected_workflow}",
        }

    g.add_node("run", run_workflow)
    g.add_node("unsupported", unsupported)
    g.set_conditional_entry_point(router, {"run": "run", "unsupported": "unsupported"})
    g.add_edge("run", END)
    g.add_edge("unsupported", END)
    return g.compile()