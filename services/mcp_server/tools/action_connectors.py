"""
Action connectors — HITL-gated, high-risk operations with external side effects.

These connectors MUST only be called when:
  1. P01 risk_tier = 'high'
  2. P02 HITL approval has been granted (approval_granted=True in context)

Any call without explicit approval raises PermissionError.
"""
from typing import Any, Dict


async def send_email(arguments: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send email (Action connector — HITL-gated).

    Flow: P01 classifies risk=high → P02 pauses at approval_gate
    → human reviews /approval/pending → POST /approval/decide (approved=true)
    → P02 resumes dispatcher → P03 calls this connector with approval_granted=True
    """
    if not context.get("approval_granted"):
        raise PermissionError(
            "Action connectors require explicit HITL approval. "
            "Submit approval via POST /approval/decide with approved=true."
        )

    # Production: integrate with SendGrid / AWS SES
    return {
        "status": "sent",
        "to": arguments.get("to"),
        "subject": arguments.get("subject"),
        "trace_id": context.get("trace_id"),
        "reviewer_id": context.get("reviewer_id"),
        "connector_type": "action",
    }
