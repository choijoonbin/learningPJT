"""Finance Agent — financial analysis, reporting, compliance checks."""
import httpx
from typing import Any, Dict
from .base import BaseDomainAgent, MCP_SERVER_URL


class FinanceAgent(BaseDomainAgent):
    domain = "finance"
    system_prompt = (
        "You are a financial analyst with expertise in enterprise accounting. "
        "Provide accurate, compliance-aware analysis. "
        "Flag any regulatory concerns and always recommend human review for transactions."
    )

    async def _call_tools(self, task: str, context: Dict[str, Any]) -> list[Dict[str, Any]]:
        """Query financial data systems via P04 MCP server."""
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.post(
                    f"{MCP_SERVER_URL}/tools/call",
                    json={
                        "tool": "finance_query",
                        "arguments": {"query": task, "tenant_id": context.get("tenant_id")},
                        "context": context,
                    },
                )
            resp.raise_for_status()
            return [resp.json()]
        except Exception:
            return []
