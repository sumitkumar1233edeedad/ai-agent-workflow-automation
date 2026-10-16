from pydantic import BaseModel, Field
from typing import Any, Optional, List, Dict

class WorkflowSpec(BaseModel):
    id: str
    name: str
    trigger: str
    inputs: List[str] = Field(default_factory=list)
    steps: List[str] = Field(default_factory=list)
    condition: str = ""
    tools: List[str] = Field(default_factory=list)
    expected_output: str = ""

class AgentState(BaseModel):
    user_request: str
    selected_workflow: Optional[str] = None
    reasoning: str = ""
    step_results: List[Dict[str, Any]] = Field(default_factory=list)
    final_output: Any = None
    error: Optional[str] = None