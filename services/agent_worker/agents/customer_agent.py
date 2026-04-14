"""Customer Agent — CRM queries, ticket management, satisfaction analysis."""
import httpx
from typing import Any, Dict
from .base import BaseDomainAgent, MCP_SERVER_URL


class CustomerAgent(BaseDomainAgent):
    domain = "customer"
    system_prompt = (
        "You are a customer success expert. "
        "Be empathetic, solution-focused, and always prioritize customer experience. "
        "Escalate to human support when the issue requires it."
    )

    async def _call_tools(self, task: str, context: Dict[str, Any]) -> list[Dict[str, Any]]:
        """Lookup CRM data via P04 MCP server."""
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.post(
                    f"{MCP_SERVER_URL}/tools/call",
                    json={
                        "tool": "crm_lookup",
                        "arguments": {"query": task, "tenant_id": context.get("tenant_id")},
                        "context": context,
                    },
                )
            resp.raise_for_status()
            return [resp.json()]
        except Exception:
            return []
