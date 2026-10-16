"""Workflow handlers package."""

from src.workflows.handlers import (
    WORKFLOW_HANDLERS,
    handle_wf001_inventory_restock,
    handle_wf002_price_validation,
    handle_wf003_vendor_processing,
    handle_wf004_product_description,
    handle_wf005_order_status,
    handle_wf006_duplicate_detection,
    handle_wf007_campaign_brief,
    handle_wf008_keyword_classification,
    handle_wf009_employee_assignment,
    handle_wf010_performance_report,
)

__all__ = [
    "WORKFLOW_HANDLERS",
    "handle_wf001_inventory_restock",
    "handle_wf002_price_validation",
    "handle_wf003_vendor_processing",
    "handle_wf004_product_description",
    "handle_wf005_order_status",
    "handle_wf006_duplicate_detection",
    "handle_wf007_campaign_brief",
    "handle_wf008_keyword_classification",
    "handle_wf009_employee_assignment",
    "handle_wf010_performance_report",
]
