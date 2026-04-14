"""LangGraph state schemas for the control plane workflow."""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
import uuid


class SubTask(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    description: str
    domain: str
    status: str = "pending"  # pending | running | done | failed
    result: Optional[Any] = None


class WorkflowInput(BaseModel):
    task: str
    domain: Optional[str] = None
    parameters: Dict[str, Any] = {}
    context: Dict[str, Any] = {}


class WorkflowState(BaseModel):
    """The mutable state that flows through LangGraph nodes."""
    input: WorkflowInput
    subtasks: List[SubTask] = []
    current_subtask_idx: int = 0
    requires_approval: bool = False
    approval_granted: Optional[bool] = None
    results: List[Any] = []
    error: Optional[str] = None
    completed: bool = False
