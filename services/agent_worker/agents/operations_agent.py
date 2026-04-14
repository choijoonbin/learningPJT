"""Operations Agent — system monitoring, alerting, incident response."""
import httpx
from typing import Any, Dict
from .base import BaseDomainAgent, MCP_SERVER_URL


class OperationsAgent(BaseDomainAgent):
    domain = "operations"
    system_prompt = (
        "You are a senior DevOps/SRE engineer. "
        "Diagnose system issues, recommend remediation steps, "
        "and always assess blast radius before suggesting actions."
    )

    async def _call_tools(self, task: str, context: Dict[str, Any]) -> list[Dict[str, Any]]:
        """Call monitoring metrics tool via P04."""
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.post(
                    f"{MCP_SERVER_URL}/tools/call",
                    json={
                        "tool": "get_metrics",
                        "arguments": {"query": task},
                        "context": context,
                    },
                )
            resp.raise_for_status()
            return [resp.json()]
        except Exception:
            return []
