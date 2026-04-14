"""
MCP tool dispatch router.
Routes tool calls to the appropriate connector based on tool name.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict

from ..tools.registry import get_tool, list_tools

router = APIRouter()


class ToolCallRequest(BaseModel):
    tool: str
    arguments: Dict[str, Any] = {}
    context: Dict[str, Any] = {}


@router.post("/call")
async def call_tool(req: ToolCallRequest):
    tool_fn = get_tool(req.tool)
    if not tool_fn:
        raise HTTPException(
            status_code=404,
            detail=f"Tool '{req.tool}' not found. Available: {list_tools()}",
        )
    try:
        result = await tool_fn(req.arguments, req.context)
        return {"tool": req.tool, "result": result}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
async def list_available_tools():
    return {"tools": list_tools()}
