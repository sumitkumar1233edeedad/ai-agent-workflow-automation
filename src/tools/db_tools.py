import json
from pathlib import Path
from typing import Union, List, Dict, Any
from .registry import tool
from ..config import get_data_path


@tool("order_lookup")
def order_lookup(order_id: str, **kwargs) -> dict:
    """Lookup order by order_id (e.g. ORD-1001) or customer email in sample_orders.json."""
    file_path = get_data_path("sample_orders.json")
    if not file_path.exists():
        return {}
    
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    target = str(order_id).strip().upper()
    if isinstance(data, list):
        for item in data:
            if item.get("order_id", "").upper() == target or item.get("customer_email", "").strip().lower() == order_id.strip().lower():
                return item
        return {}
    elif isinstance(data, dict):
        return data.get(order_id) or data.get(target) or {}
    return {}


@tool("employee_lookup")
def employee_lookup(employee_id: str = None, **kwargs) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    """Lookup employees in sample_employees.json."""
    file_path = get_data_path("sample_employees.json")
    if not file_path.exists():
        return []
    
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if employee_id and isinstance(data, list):
        for emp in data:
            if emp.get("employee_id") == employee_id:
                return emp
        return {}
    return data