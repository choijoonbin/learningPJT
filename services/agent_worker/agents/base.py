"""
BaseDomainAgent — abstract base class for all domain agents.

Every domain agent:
1. Receives a task string + context envelope
2. Optionally queries P04 (MCP tools) and P05 (knowledge)
3. Calls the LLM via LiteLLM
4. Returns a structured result dict
"""
from abc import ABC, abstractmethod
from typing import Any, Dict
import os
import httpx
import litellm

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8002")
KNOWLEDGE_API_URL = os.getenv("KNOWLEDGE_API_URL", "http://localhost:8003")
LITELLM_MODEL = os.getenv("LITELLM_MODEL", "anthropic/claude-sonnet-4-6")


class BaseDomainAgent(ABC):
    """Base class for domain-specific agents."""

    domain: str = "base"
    system_prompt: str = "You are a helpful AI assistant."

    async def execute(self, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Run the agent: tool calls → LLM → structured response."""
        # 1. Retrieve relevant knowledge from P05
        knowledge = await self._retrieve_knowledge(task, context)

        # 2. Call domain-specific tools from P04
        tool_results = await self._call_tools(task, context)

        # 3. Build prompt and call LLM
        response = await self._call_llm(task, knowledge, tool_results, context)

        return {
            "domain": self.domain,
            "task": task,
            "response": response,
            "knowledge_used": len(knowledge) > 0,
            "tools_used": len(tool_results) > 0,
            "trace_id": context.get("trace_id"),
        }

    @abstractmethod
    async def _call_tools(
        self, task: str, context: Dict[str, Any]
    ) -> list[Dict[str, Any]]:
        """Override to call domain-specific tools via P04 MCP server."""
        return []

    async def _retrieve_knowledge(
        self, task: str, context: Dict[str, Any]
    ) -> list[str]:
        """Query P05 knowledge API for relevant context."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    f"{KNOWLEDGE_API_URL}/knowledge/search",
                    json={"query": task, "top_k": 3, "tenant_id": context.get("tenant_id", "default")},
                )
            resp.raise_for_status()
            return [r["content"] for r in resp.json().get("results", [])]
        except Exception:
            return []

    async def _call_llm(
        self,
        task: str,
        knowledge: list[str],
        tool_results: list[Dict[str, Any]],
        context: Dict[str, Any],
    ) -> str:
        knowledge_block = "\n".join(f"- {k}" for k in knowledge) if knowledge else "None"
        tool_block = "\n".join(str(t) for t in tool_results) if tool_results else "None"

        messages = [
            {
                "role": "system",
                "content": self.system_prompt,
            },
            {
                "role": "user",
                "content": (
                    f"Task: {task}\n\n"
                    f"Relevant Knowledge:\n{knowledge_block}\n\n"
                    f"Tool Results:\n{tool_block}\n\n"
                    f"Tenant: {context.get('tenant_id')}, "
                    f"Risk Tier: {context.get('risk_tier', 'low')}\n\n"
                    "Provide a concise, structured response."
                ),
            },
        ]

        response = await litellm.acompletion(
            model=LITELLM_MODEL,
            messages=messages,
            max_tokens=1024,
        )
        return response.choices[0].message.content
