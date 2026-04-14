"""
LangGraph workflow assembly.
Builds the StateGraph and runs it end-to-end.
"""
from langgraph.graph import StateGraph, END
from .nodes import planner_node, approval_gate_node, dispatcher_node, aggregator_node
from ..state.schema import WorkflowState, WorkflowInput


def build_graph() -> StateGraph:
    graph = StateGraph(WorkflowState)

    graph.add_node("planner", planner_node)
    graph.add_node("approval_gate", approval_gate_node)
    graph.add_node("dispatcher", dispatcher_node)
    graph.add_node("aggregator", aggregator_node)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "approval_gate")

    # Conditional edge: skip dispatcher if waiting for approval
    def route_after_approval(state: WorkflowState) -> str:
        if state.approval_granted is None:
            return END  # Pause — waiting for HITL
        if state.approval_granted is False:
            return END  # Rejected
        return "dispatcher"

    graph.add_conditional_edges("approval_gate", route_after_approval)
    graph.add_edge("dispatcher", "aggregator")
    graph.add_edge("aggregator", END)

    return graph.compile()


_compiled_graph = None


def get_graph():
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_graph()
    return _compiled_graph


async def run_workflow(input_data: WorkflowInput) -> dict:
    graph = get_graph()
    initial_state = WorkflowState(input=input_data)
    final_state = await graph.ainvoke(initial_state)

    if isinstance(final_state, WorkflowState):
        fs = final_state
    else:
        fs = WorkflowState(**final_state)

    return {
        "session_id": fs.input.context.get("session_id"),
        "completed": fs.completed,
        "requires_approval": fs.requires_approval,
        "approval_granted": fs.approval_granted,
        "results": fs.results,
        "subtask_count": len(fs.subtasks),
    }
