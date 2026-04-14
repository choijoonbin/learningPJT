"""HITL approval router — human reviewer submits approve/reject."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..state.redis_checkpoint import get_pending_approval, resolve_approval

router = APIRouter()


class ApprovalDecision(BaseModel):
    session_id: str
    approved: bool
    reviewer_id: str
    reason: str | None = None

from typing import Optional


@router.get("/pending/{session_id}")
async def get_pending(session_id: str):
    data = await get_pending_approval(session_id)
    if not data:
        raise HTTPException(status_code=404, detail="No pending approval found")
    return data


@router.post("/decide")
async def decide(decision: ApprovalDecision):
    ok = await resolve_approval(
        session_id=decision.session_id,
        approved=decision.approved,
        reviewer_id=decision.reviewer_id,
        reason=decision.reason,
    )
    if not ok:
        raise HTTPException(status_code=404, detail="Session not found or already resolved")
    return {"status": "resolved", "approved": decision.approved}
