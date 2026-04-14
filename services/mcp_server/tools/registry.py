"""Tool registry — maps tool names to async connector functions."""
from .read_connectors import web_search, get_metrics, crm_lookup, finance_query
from .write_connectors import db_write, create_ticket
from .action_connectors import send_email
from typing import Callable, Optional

_registry: dict[str, Callable] = {
    # Read connectors (auto-approved)
    "web_search":    web_search,
    "get_metrics":   get_metrics,
    "crm_lookup":    crm_lookup,
    "finance_query": finance_query,
    # Write connectors (RBAC-checked)
    "db_write":      db_write,
    "create_ticket": create_ticket,
    # Action connectors (HITL-gated)
    "send_email":    send_email,
}


def get_tool(name: str) -> Optional[Callable]:
    return _registry.get(name)


def list_tools() -> list[str]:
    return list(_registry.keys())
