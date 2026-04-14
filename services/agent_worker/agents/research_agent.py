"""Research Agent — information gathering and synthesis."""
import httpx
import os
from typing import Any, Dict
from .base import BaseDomainAgent, MCP_SERVER_URL


class ResearchAgent(BaseDomainAgent):
    domain = "research"
    system_prompt = (
        "You are an expert research analyst. "
        "Synthesize information clearly, cite sources when available, "
        "and highlight key insights with confidence levels."
    )

    async def _call_tools(self, task: str, context: Dict[str, Any]) -> list[Dict[str, Any]]:
        """Query web search tool via P04 MCP server."""
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.post(
                    f"{MCP_SERVER_URL}/tools/call",
                    json={
                        "tool": "web_search",
                        "arguments": {"query": task},
                        "context": context,
                    },
                )
            resp.raise_for_status()
            return [resp.json()]
        except Exception:
            return []
