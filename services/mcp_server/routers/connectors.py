"""Connector inventory endpoint."""
from fastapi import APIRouter

router = APIRouter()

CONNECTORS = [
    {"name": "web_search",    "type": "read",   "description": "Web search (read-only)"},
    {"name": "get_metrics",   "type": "read",   "description": "Prometheus metrics query"},
    {"name": "crm_lookup",    "type": "read",   "description": "CRM customer lookup"},
    {"name": "finance_query", "type": "read",   "description": "Financial data query"},
    {"name": "db_write",      "type": "write",  "description": "Database write (RBAC-gated)"},
    {"name": "create_ticket", "type": "write",  "description": "Create support ticket"},
    {"name": "send_email",    "type": "action", "description": "Send email (HITL-gated)"},
]


@router.get("/list")
async def list_connectors():
    return {"connectors": CONNECTORS}
