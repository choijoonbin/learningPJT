"""
Redis-backed checkpoint store for durable workflow state.
Supports pause/resume for HITL approval flows.
"""
import json
import os
from typing import Any, Dict, Optional
import redis.asyncio as aioredis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CHECKPOINT_TTL = 3600 * 24  # 24 hours

_redis: Optional[aioredis.Redis] = None


async def init_redis():
    global _redis
    _redis = await aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)


def _get_redis() -> aioredis.Redis:
    if _redis is None:
        raise RuntimeError("Redis not initialized. Call init_redis() first.")
    return _redis


async def save_checkpoint(session_id: str, state: Dict[str, Any]) -> None:
    r = _get_redis()
    await r.setex(f"checkpoint:{session_id}", CHECKPOINT_TTL, json.dumps(state))


async def load_checkpoint(session_id: str) -> Optional[Dict[str, Any]]:
    r = _get_redis()
    data = await r.get(f"checkpoint:{session_id}")
    return json.loads(data) if data else None


async def save_pending_approval(session_id: str, payload: Dict[str, Any]) -> None:
    r = _get_redis()
    await r.setex(f"approval:{session_id}", CHECKPOINT_TTL, json.dumps(payload))


async def get_pending_approval(session_id: str) -> Optional[Dict[str, Any]]:
    r = _get_redis()
    data = await r.get(f"approval:{session_id}")
    return json.loads(data) if data else None


async def resolve_approval(
    session_id: str,
    approved: bool,
    reviewer_id: str,
    reason: Optional[str],
) -> bool:
    r = _get_redis()
    data = await r.get(f"approval:{session_id}")
    if not data:
        return False
    payload = json.loads(data)
    payload["approved"] = approved
    payload["reviewer_id"] = reviewer_id
    payload["reason"] = reason
    payload["resolved"] = True
    await r.setex(f"approval:{session_id}", CHECKPOINT_TTL, json.dumps(payload))
    return True
