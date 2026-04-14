"""Agent dispatch router."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, Optional

from ..agents.registry import get_agent

router = APIRouter()

DOMAIN_MAP = {
    "research": "research",
    "operations": "operations",
    "ops": "operations",
    "customer": "customer",
    "finance": "finance",
    None: "research",
}


class AgentRunRequest(BaseModel):
    task: str
    domain: Optional[str] = None
    context: Dict[str, Any] = {}


@router.post("/run")
async def run_agent(req: AgentRunRequest):
    domain = DOMAIN_MAP.get(req.domain, "research")
    agent = get_agent(domain)
    if not agent:
        raise HTTPException(status_code=400, detail=f"Unknown domain: {domain}")

    try:
        result = await agent.execute(
            task=req.task,
            context=req.context,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
