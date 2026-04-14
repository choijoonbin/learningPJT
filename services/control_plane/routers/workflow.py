"""Workflow router — accepts tasks and runs LangGraph workflow."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, Optional

from ..graph.workflow import run_workflow
from ..state.schema import WorkflowInput

router = APIRouter()


class WorkflowRequest(BaseModel):
    task: str
    domain: Optional[str] = None
    parameters: Dict[str, Any] = {}
    context: Dict[str, Any] = {}  # ContextEnvelope as dict


@router.post("/run")
async def run(req: WorkflowRequest):
    try:
        result = await run_workflow(
            WorkflowInput(
                task=req.task,
                domain=req.domain,
                parameters=req.parameters,
                context=req.context,
            )
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
