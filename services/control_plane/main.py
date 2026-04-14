"""
P02 — Control Plane
LangGraph-based orchestrator that manages multi-step agent workflows.
Responsibilities:
  - Task planning (decompose into subtasks)
  - State management with Redis checkpoint
  - HITL approval gate (conditional, high-risk only)
  - Agent dispatch to P03 worker
  - Audit logging
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from .routers import workflow, approval, health
from .state.redis_checkpoint import init_redis

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("P02 Control Plane starting up")
    await init_redis()
    yield
    logger.info("P02 Control Plane shutting down")


app = FastAPI(
    title="P02 — Control Plane",
    description="LangGraph orchestrator with durable state, HITL approval, and agent dispatch",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(workflow.router, prefix="/workflow", tags=["workflow"])
app.include_router(approval.router, prefix="/approval", tags=["approval"])
app.include_router(health.router, tags=["health"])
