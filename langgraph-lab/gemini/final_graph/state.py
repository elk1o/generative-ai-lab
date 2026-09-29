import operator
from typing import TypedDict, Annotated, List, Literal

# Setting up State
class FinalDraftState(TypedDict):
    message: str
    draft: str
    intent: Literal["ventas", "soporte", "general"]
    initial_data_tries: int
    draft_edit_tries: int
    initial_data_user_decision: Literal["OK", "KO"]
    draft_user_decision: Literal["OK", "KO", "EDIT"]
    short_message: str
    keywords: List[str]
    urgency: Literal["CRÍTICA","ALTA","MEDIA","BAJA"]
    respuesta_final: str
    # setting up the scratchpad to record nodes exec order
    log: Annotated[List[str], operator.add]