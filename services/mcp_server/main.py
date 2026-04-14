"""
P04 — Shared Integration Layer (MCP Server)
FastMCP-based tool gateway that provides unified tool access to all domain agents.

Connector model:
  - Read connectors  : auto-approved, no side effects
  - Write connectors : RBAC-checked, require analyst role+
  - Action connectors: HITL-gated, require explicit approval from P02
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from .routers import tools, connectors, health

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("P04 MCP Server starting up")
    yield
    logger.info("P04 MCP Server shutting down")


app = FastAPI(
    title="P04 — Shared Integration Layer",
    description="FastMCP tool gateway: Read / Write / Action connectors",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(tools.router, prefix="/tools", tags=["tools"])
app.include_router(connectors.router, prefix="/connectors", tags=["connectors"])
app.include_router(health.router, tags=["health"])
