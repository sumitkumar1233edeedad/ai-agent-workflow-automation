"""Command-Line Interface for AI Agent Workflow Automation."""

import sys
import json
import argparse
from typing import Optional

# Ensure UTF-8 output on Windows terminals
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from .config import load_workflows
from .selector import select_workflow
from .executor import build_graph
from .models import AgentState


def print_banner():
    print("=" * 60)
    print("  AI Agent Workflow Automation System")
    print("  Powered by LangGraph & LangChain ChatOpenAI")
    print("=" * 60)


def list_workflows():
    workflows = load_workflows()
    print("\n[CATALOG] Available Business Workflows:")
    print("-" * 60)
    for wid, w in workflows.items():
        print(f"[{w.id}] {w.name}")
        print(f"  Trigger : {w.trigger}")
        print(f"  Tools   : {', '.join(w.tools)}")
        print(f"  Rule    : {w.condition}")
        print()


def run_request(request_text: str, forced_workflow: Optional[str] = None, json_mode: bool = False, verbose: bool = False):
    workflows = load_workflows()
    
    if forced_workflow:
        wid = forced_workflow.upper()
        reasoning = f"Manually overridden to {wid}"
        if wid not in workflows:
            print(f"[ERROR] Workflow ID '{wid}' not found in specification catalog.")
            return
    else:
        wid, reasoning = select_workflow(request_text, workflows)

    w_name = workflows[wid].name if wid in workflows else "Unrecognized Workflow"
    
    if not json_mode:
        print(f"\n>>> Selected Workflow: {wid} - {w_name}")
        print(f"    Routing Logic: {reasoning}\n")

    graph = build_graph()
    state = AgentState(user_request=request_text, selected_workflow=wid, reasoning=reasoning)
    out = graph.invoke(state)

    if json_mode:
        print(json.dumps(out, indent=2, default=str))
        return

    print(">>> Steps Executed:")
    for step in out.get("step_results", []):
        st = step.get("status", "SUCCESS")
        sname = step.get("step", "step")
        details = ", ".join(f"{k}={v}" for k, v in step.items() if k not in ["step", "status"])
        print(f"   [{st}] {sname}" + (f" ({details})" if details else ""))

    print("\n>>> Workflow Output:")
    final = out.get("final_output")
    if isinstance(final, (dict, list)):
        print(json.dumps(final, indent=2, default=str))
    else:
        print(final)

    if out.get("error"):
        print(f"\n[ALERT] Execution Error: {out['error']}")


def main():
    parser = argparse.ArgumentParser(description="AI Agent Workflow Automation CLI")
    parser.add_argument("query", nargs="*", help="Natural language workflow request")
    parser.add_argument("--list", "-l", action="store_true", help="List all configured workflows")
    parser.add_argument("--workflow", "-w", type=str, default=None, help="Force a specific workflow ID (e.g. WF001)")
    parser.add_argument("--json", "-j", action="store_true", help="Output state machine state as JSON")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show verbose logs")

    args = parser.parse_args()

    if args.list:
        list_workflows()
        return

    req = " ".join(args.query).strip()
    if not req:
        print_banner()
        try:
            req = input("\nEnter your workflow request: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            return

    if not req:
        print("[WARN] No request provided. Use --list to see available workflows.")
        return

    run_request(req, forced_workflow=args.workflow, json_mode=args.json, verbose=args.verbose)


if __name__ == "__main__":
    main()