"""
P03 — Domain Agent Runtime
Hosts domain-specific agents (Research, Operations, Customer, Finance).
Each agent extends BaseDomainAgent and implements the execute() method.
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from .routers import agent, health

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("P03 Agent Worker starting up")
    yield
    logger.info("P03 Agent Worker shutting down")


app = FastAPI(
    title="P03 — Domain Agent Runtime",
    description="Domain-specific agents: Research, Operations, Customer, Finance",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(agent.router, prefix="/agent", tags=["agent"])
app.include_router(health.router, tags=["health"])
