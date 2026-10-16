import sys
from pathlib import Path

# Ensure project root is in sys.path so it runs standalone from any terminal
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    import pytest
except ImportError:
    pytest = None

from src.config import load_workflows
from src.selector import select_workflow
from src.executor import build_graph
from src.models import AgentState

CASES = [
    ("Which products need restocking?", "WF001"),
    ("Find products where vendor price differs by more than 10%.", "WF002"),
    ("Process this vendor spreadsheet and show invalid rows.", "WF003"),
    ("Generate SEO content for this product.", "WF004"),
    ("Where is order ORD-1001?", "WF005"),
    ("Find likely duplicate products in the catalog.", "WF006"),
    ("Create a campaign brief for the new collection.", "WF007"),
    ("Classify these keywords and map them to pages.", "WF008"),
    ("Assign this urgent task to the best available developer.", "WF009"),
    ("Which workflows are failing most often?", "WF010"),
]

def run_single_case(req: str, expected: str):
    wfs = load_workflows()
    wid, reason = select_workflow(req, wfs)
    assert wid == expected, f"Router picked {wid}, expected {expected} ({reason})"
    graph = build_graph()
    out = graph.invoke(AgentState(user_request=req, selected_workflow=wid))
    assert out.get("final_output") is not None, f"Final output was None for {expected}"
    assert out.get("error") is None, f"Execution failed for {expected}: {out.get('error')}"
    return out

if pytest is not None:
    @pytest.mark.parametrize("req,expected", CASES)
    def test_routing_and_execution(req, expected):
        run_single_case(req, expected)

if __name__ == "__main__":
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print("=" * 65)
    print("  Manual Execution Test: All 10 Business Workflows")
    print("=" * 65)
    wfs = load_workflows()
    passed = 0

    for i, (req, expected) in enumerate(CASES, 1):
        print(f"\n[{i}/10] Testing {expected}: '{req}'")
        try:
            out = run_single_case(req, expected)
            steps = out.get("step_results", [])
            print(f"  --> PASSED [OK]")
            print(f"      Steps executed: {len(steps)}")
            passed += 1
        except Exception as exc:
            print(f"  --> FAILED [X]: {exc}")

    print("\n" + "=" * 65)
    print(f"  Summary: {passed}/{len(CASES)} Workflows Passed Successfully")
    print("=" * 65)