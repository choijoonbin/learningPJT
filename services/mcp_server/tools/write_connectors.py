"""
Write connectors — RBAC-checked, require analyst role or above.
These connectors have side effects (DB writes, ticket creation).
"""
from typing import Any, Dict
import uuid


async def db_write(arguments: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Database write (Write connector).
    RBAC: analyst role or higher required.
    """
    role = context.get("role", "viewer")
    if role not in ("analyst", "admin"):
        raise PermissionError(
            f"Role '{role}' cannot use write connectors. "
            "Analyst or admin role required."
        )
    return {
        "status": "written",
        "record_id": str(uuid.uuid4())[:8],
        "table": arguments.get("table", "unknown"),
        "trace_id": context.get("trace_id"),
        "connector_type": "write",
    }


async def create_ticket(arguments: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create support ticket (Write connector).
    Production: integrate with Jira / ServiceNow API.
    """
    return {
        "ticket_id": f"TICK-{str(uuid.uuid4())[:6].upper()}",
        "status": "created",
        "subject": arguments.get("subject", ""),
        "priority": arguments.get("priority", "medium"),
        "trace_id": context.get("trace_id"),
        "connector_type": "write",
    }
