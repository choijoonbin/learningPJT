"""
LangGraph node definitions for the P02 Control Plane workflow.

Graph topology:
  planner → approval_gate (conditional) → dispatcher → aggregator
                  ↓ (high-risk)
              [wait for HITL]
                  ↓ (approved)
              dispatcher
"""
import os
import json
import httpx
from typing import Any
from ..state.schema import WorkflowState, SubTask
from ..state.redis_checkpoint import save_checkpoint, save_pending_approval

AGENT_WORKER_URL = os.getenv("AGENT_WORKER_URL", "http://localhost:8004")
REQUIRE_HITL_ABOVE = float(os.getenv("REQUIRE_HITL_ABOVE", "0.8"))


async def planner_node(state: WorkflowState) -> WorkflowState:
    """
    Decompose the top-level task into subtasks.
    Uses rule-based decomposition (swap with LLM planner for production).
    """
    task = state.input.task
    domain = state.input.domain or "research"
    risk_score = state.input.context.get("metadata", {}).get("risk_score", 0.0)

    # Simple domain-based decomposition
    subtasks = [
        SubTask(description=f"Gather context for: {task}", domain="research"),
        SubTask(description=f"Analyze and synthesize: {task}", domain=domain),
    ]
    if "report" in task.lower() or "summary" in task.lower():
        subtasks.append(SubTask(description="Generate final report", domain="research"))

    state.subtasks = subtasks
    state.requires_approval = risk_score >= REQUIRE_HITL_ABOVE

    await save_checkpoint(
        state.input.context.get("session_id", "unknown"),
        state.model_dump(),
    )
    return state


async def approval_gate_node(state: WorkflowState) -> WorkflowState:
    """
    Conditional HITL gate — only blocks when requires_approval=True.
    Saves pending approval to Redis; waits for /approval/decide callback.
    """
    if not state.requires_approval:
        state.approval_granted = True
        return state

    session_id = state.input.context.get("session_id", "unknown")
    await save_pending_approval(
        session_id,
        {
            "session_id": session_id,
            "task": state.input.task,
            "risk_score": state.input.context.get("metadata", {}).get("risk_score"),
            "subtasks": [s.model_dump() for s in state.subtasks],
            "resolved": False,
            "approved": None,
        },
    )
    # In a real implementation this would use LangGraph's interrupt()
    # For the lab: approval must be POSTed to /approval/decide
    state.approval_granted = None  # Signals "waiting"
    return state


async def dispatcher_node(state: WorkflowState) -> WorkflowState:
    """
    Dispatches each subtask to the P03 Agent Worker.
    Runs subtasks sequentially; extend to parallel with asyncio.gather.
    """
    for subtask in state.subtasks:
        subtask.status = "running"
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(
                    f"{AGENT_WORKER_URL}/agent/run",
                    json={
                        "task": subtask.description,
                        "domain": subtask.domain,
                        "context": state.input.context,
                    },
                )
            resp.raise_for_status()
            subtask.result = resp.json()
            subtask.status = "done"
        except Exception as e:
            subtask.result = {"error": str(e)}
            subtask.status = "failed"

        state.results.append(subtask.result)

    return state


async def aggregator_node(state: WorkflowState) -> WorkflowState:
    """Merge subtask results into final response."""
    successful = [r for r in state.results if "error" not in r]
    failed = [r for r in state.results if "error" in r]

    state.completed = True
    state.input.parameters["_aggregated"] = {
        "total": len(state.results),
        "successful": len(successful),
        "failed": len(failed),
        "results": successful,
    }
    return state
