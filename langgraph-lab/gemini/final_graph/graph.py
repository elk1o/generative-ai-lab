from langgraph.graph import StateGraph, END, START
from typing import Literal
from state import FinalDraftState
from constants import MAX_ASK_EDITION_ATTEMPTS, MAX_DRAFT_EDITION_ATTEMPTS
from nodes import recibe_customer_message, clasify_user_intent, send_soporte_answer, send_informacion_general_answer,\
    validate_initial_data, modify_initial_data, setup_analysis, setup_urgency, extract_keywords, summary_user_message,\
        generate_AI_draft, validate_draft, send_draft, end_without_send, modify_draft

# Creating graph
workflow = StateGraph(FinalDraftState)

# Creating nodes
workflow.add_node("recibe_customer_message",recibe_customer_message)
workflow.add_node("clasify_user_intent",clasify_user_intent)
workflow.add_node("send_soporte_answer",send_soporte_answer)
workflow.add_node("send_informacion_general_answer",send_informacion_general_answer)
workflow.add_node("validate_initial_data",validate_initial_data)
workflow.add_node("modify_initial_data",modify_initial_data)
workflow.add_node("setup_analysis",setup_analysis)
workflow.add_node("setup_urgency",setup_urgency)
workflow.add_node("extract_keywords",extract_keywords)
workflow.add_node("summary_user_message",summary_user_message)
workflow.add_node("generate_AI_draft",generate_AI_draft)
workflow.add_node("validate_draft",validate_draft)
workflow.add_node("send_draft",send_draft)
workflow.add_node("end_without_send",end_without_send)
workflow.add_node("modify_draft",modify_draft)

def router_classify_user_intent(state: FinalDraftState) -> Literal["ventas", "soporte", "general"]:
    return state["intent"]

def router_validate_initial_data(state: FinalDraftState) -> Literal["OK", "KO", "EDIT"]:
    # validacion de attempts
    if state["initial_data_user_decision"] == "KO":
        return "KO" if state["initial_data_tries"] >= MAX_ASK_EDITION_ATTEMPTS else "EDIT"
    return state["initial_data_user_decision"]

def router_validate_draft(state: FinalDraftState) -> Literal["OK", "KO", "EDIT"]:
    # validacion de attempts
    if state["draft_user_decision"] == "EDIT" and state["draft_edit_tries"] >= MAX_DRAFT_EDITION_ATTEMPTS:
        return "KO"
    return state["draft_user_decision"]

# Creating edges
workflow.add_edge(START, "recibe_customer_message")
workflow.add_edge("recibe_customer_message", "validate_initial_data")
workflow.add_conditional_edges(
    "validate_initial_data",
    router_validate_initial_data,
    {
        "OK": "clasify_user_intent",
        "EDIT": "modify_initial_data",
        "KO": "end_without_send"
    }
)
workflow.add_edge("modify_initial_data", "validate_initial_data")
workflow.add_conditional_edges(
    "clasify_user_intent",
    router_classify_user_intent,
    {
        "ventas": "setup_analysis",
        "soporte": "send_soporte_answer",
        "general": "send_informacion_general_answer",
    }
)
workflow.add_edge("send_soporte_answer", END)
workflow.add_edge("send_informacion_general_answer", END)
workflow.add_edge("setup_analysis", "setup_urgency")
workflow.add_edge("setup_analysis", "extract_keywords")
workflow.add_edge("setup_analysis", "summary_user_message")
workflow.add_edge(["setup_urgency", "extract_keywords", "summary_user_message"], "generate_AI_draft")
workflow.add_edge("generate_AI_draft", "validate_draft")
workflow.add_conditional_edges(
    "validate_draft",
    router_validate_draft,
    {
        "OK": "send_draft",
        "EDIT": "modify_draft",
        "KO": "end_without_send"
    }
)
# workflow.add_edge(["send_draft","end_without_send"], END) Not specifically parallel edges
workflow.add_edge("modify_draft", "validate_draft")
workflow.add_edge("send_draft", END)
workflow.add_edge("end_without_send", END)
