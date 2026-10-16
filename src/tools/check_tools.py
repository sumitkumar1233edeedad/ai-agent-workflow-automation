"""Script to manually verify each individual registered tool."""

import sys
import json

# Ensure UTF-8 output
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from src.tools import call_tool, TOOLS
from src.config import get_data_path


def test_all_tools():
    print("=" * 60)
    print("  Tool Registry Diagnostics: Verifying All Registered Tools")
    print("=" * 60)
    print(f"Total Registered Tools: {len(TOOLS)}")
    print(f"Tools list: {', '.join(TOOLS.keys())}\n")

    results = {}

    # 1. csv_reader
    try:
        df = call_tool("csv_reader", path="sample_inventory.csv")
        results["csv_reader"] = f"OK (Loaded {len(df)} rows from sample_inventory.csv)"
    except Exception as e:
        results["csv_reader"] = f"FAILED: {e}"

    # 2. excel_parser
    try:
        df = call_tool("excel_parser", path="sample_vendor_products.csv")
        results["excel_parser"] = f"OK (Parsed {len(df)} rows from spreadsheet)"
    except Exception as e:
        results["excel_parser"] = f"FAILED: {e}"

    # 3. calculator
    try:
        res = call_tool("calculator", expr="15 * 2 - 4")
        results["calculator"] = f"OK (15 * 2 - 4 = {res})"
    except Exception as e:
        results["calculator"] = f"FAILED: {e}"

    # 4. order_lookup
    try:
        order = call_tool("order_lookup", order_id="ORD-1001")
        if order and "customer_name" in order:
            results["order_lookup"] = f"OK (Found ORD-1001 for {order['customer_name']})"
        else:
            results["order_lookup"] = "FAILED: Order not found"
    except Exception as e:
        results["order_lookup"] = f"FAILED: {e}"

    # 5. employee_lookup
    try:
        emps = call_tool("employee_lookup")
        results["employee_lookup"] = f"OK (Retrieved {len(emps)} employee records)"
    except Exception as e:
        results["employee_lookup"] = f"FAILED: {e}"

    # 6. llm (LangChain ChatOpenAI)
    try:
        resp = call_tool("llm", prompt="Respond with ONLY the word: ToolVerified")
        results["llm"] = f"OK (Response: {resp[:40]}...)"
    except Exception as e:
        results["llm"] = f"FAILED: {e}"

    # 7. report_tools: flag_threshold
    try:
        df = call_tool("csv_reader", path="sample_inventory.csv")
        low = call_tool("flag_threshold", df=df, column="current_stock", threshold=10, op="<")
        results["flag_threshold"] = f"OK (Flagged {len(low)} items with stock < 10)"
    except Exception as e:
        results["flag_threshold"] = f"FAILED: {e}"

    # 8. report_tools: summary_stats
    try:
        df = call_tool("csv_reader", path="sample_inventory.csv")
        stats = call_tool("summary_stats", df=df, column="current_stock")
        results["summary_stats"] = f"OK (Mean stock: {stats.get('mean')}, Count: {stats.get('count')})"
    except Exception as e:
        results["summary_stats"] = f"FAILED: {e}"

    # 9. report_tools: to_json
    try:
        j_str = call_tool("to_json", obj={"status": "active", "code": 200})
        results["to_json"] = f"OK (Serialized valid JSON string)"
    except Exception as e:
        results["to_json"] = f"FAILED: {e}"

    print("-" * 60)
    for tool_name, status in results.items():
        icon = "[PASS]" if status.startswith("OK") else "[FAIL]"
        print(f" {icon:<7} {tool_name:<20} -> {status}")
    print("-" * 60)
    all_ok = all(v.startswith("OK") for v in results.values())
    if all_ok:
        print("\nAll tested tools are operational and working properly! ✅\n")
    else:
        print("\nSome tools encountered issues. Please check logs above. ❌\n")


if __name__ == "__main__":
    test_all_tools()
