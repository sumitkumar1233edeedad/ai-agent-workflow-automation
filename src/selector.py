"""Workflow router using LangChain ChatOpenAI with precision fallback."""

import os
import re
from typing import Optional
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage

from .models import WorkflowSpec
from .llm import get_chat_model

load_dotenv()

SYSTEM_PROMPT = """You are an enterprise AI workflow router.
Given the user request and the list of available workflows, return ONLY the exact matching Workflow ID (e.g. WF001, WF002, ..., WF010).
Do not include punctuation, reasoning, or quotes.
If nothing matches, return 'NONE'."""

# Deterministic keywords fallback for offline / safety resilience
TRIGGER_PATTERNS = [
    ("WF001", [r"restock", r"inventory.*low", r"need.*restock", r"current_stock"]),
    ("WF002", [r"price.*differ", r"vendor price", r"variance", r"price.*validation", r"differs by more than"]),
    ("WF003", [r"vendor spreadsheet", r"invalid rows", r"vendor file", r"vendor upload"]),
    ("WF004", [r"seo content", r"product description", r"product content", r"generate seo"]),
    ("WF005", [r"order\s+ord-\d+", r"where is order", r"order status", r"ord-\d+"]),
    ("WF006", [r"duplicate", r"duplicate product", r"duplicates in the catalog"]),
    ("WF007", [r"campaign brief", r"campaign.*collection", r"marketing campaign"]),
    ("WF008", [r"keyword", r"keywords", r"search intent", r"classify.*keyword"]),
    ("WF009", [r"assign.*task", r"best available developer", r"assign.*developer", r"task assignment"]),
    ("WF010", [r"failing most often", r"workflow.*fail", r"performance report", r"sla breach"]),
]


def _fallback_match(user_request: str, workflows: dict[str, WorkflowSpec]) -> Optional[str]:
    low = user_request.lower().strip()
    for wid, patterns in TRIGGER_PATTERNS:
        if wid in workflows:
            for pat in patterns:
                if re.search(pat, low):
                    return wid
    return None


def select_workflow(user_request: str, workflows: dict[str, WorkflowSpec]) -> tuple[str, str]:
    """
    Select the best workflow ID using LangChain's ChatOpenAI model.
    Falls back to semantic/trigger matching if LLM is unavailable or yields invalid ID.
    """
    catalog = "\n".join(
        f"- {w.id} | {w.name} | Trigger: {w.trigger}"
        for w in workflows.values()
    )

    llm = get_chat_model(temperature=0)
    selected_id = None
    reasoning = ""

    if llm:
        try:
            messages = [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=f"AVAILABLE WORKFLOWS:\n{catalog}\n\nUSER REQUEST: {user_request}"),
            ]
            resp = llm.invoke(messages)
            text = resp.content.strip() if hasattr(resp, "content") else str(resp).strip()
            
            # Extract workflow ID like WF001..WF010
            match = re.search(r"WF\d{3}", text, re.IGNORECASE)
            if match:
                candidate = match.group(0).upper()
                if candidate in workflows:
                    selected_id = candidate
                    reasoning = f"Matched via LangChain ChatOpenAI router ({candidate})"
        except Exception as e:
            reasoning = f"LangChain ChatOpenAI call failed ({e}); falling back to trigger rule matching."

    # Fallback if LLM was unavailable or did not identify a valid workflow
    if not selected_id or selected_id not in workflows:
        fallback_id = _fallback_match(user_request, workflows)
        if fallback_id and fallback_id in workflows:
            selected_id = fallback_id
            reasoning = f"Matched via semantic trigger rule ({fallback_id})"
        else:
            selected_id = "NONE"
            reasoning = "No matching workflow identified for query"

    return selected_id, reasoning