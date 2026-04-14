"""Agent registry — maps domain names to agent instances."""
from .research_agent import ResearchAgent
from .operations_agent import OperationsAgent
from .customer_agent import CustomerAgent
from .finance_agent import FinanceAgent
from .base import BaseDomainAgent
from typing import Optional

_registry = {
    "research": ResearchAgent(),
    "operations": OperationsAgent(),
    "customer": CustomerAgent(),
    "finance": FinanceAgent(),
}


def get_agent(domain: str) -> Optional[BaseDomainAgent]:
    return _registry.get(domain)


def list_agents() -> list[str]:
    return list(_registry.keys())
