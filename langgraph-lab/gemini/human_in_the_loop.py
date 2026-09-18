import operator
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Annotated, List, Literal
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, END, START
from langgraph.types import interrupt, Command

load_dotenv()
AISTUDIO_APIKEY = os.getenv('AISTUDIO_APIKEY')
DB_FILE = os.getenv('DB_FILE')
THREAD_ID = "client-hitl"
USER_PROMPT = """
    Hola, quiero saber si tienen soporte técnico disponible los fines de semana y cuál es el coste adicional por eso
"""
MAX_EDITION_ATTEMPTS = 2

llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        temperature=0,
        google_api_key=AISTUDIO_APIKEY,
        timeout=60,
        max_retries=3,
    )

# Setting up State
class DraftState(TypedDict):
    message: str
    intent: str
    draft: str
    user_decision: Literal["OK", "KO", "EDIT"]
    edit_attempts: int
    respuesta_final: str
    # setting up the scratchpad to record nodes exec order
    steps: Annotated[List[str], operator.add]

def recibe_customer_message(state: DraftState) -> dict:
    """
    Setting up user prompt
    """
    print("Superstep 2: Mensaje de input de usuario:")
    print(USER_PROMPT)
    return {
        "steps":["Recibir mensaje de usuario"]
    }

def clasify_user_intent(state: DraftState) -> dict:
    """
    Clasify user intent by message
    """
    print("Superstep 3: Clasificar la intención del usuario:")

    llm_prompt = f"""
    Clasifica la intención del siguiente mensaje de un cliente en EXACTAMENTE una de estas categorías: ventas, soporte, general
    
    - "ventas" si pregunta por precios, planes, demos, compras o cotizaciones
    - "soporte" si reporta un problema, error, o algo que no funciona
    - "general" si no encaja claramente en las anteriores
    
    Responde ÚNICAMENTE con una palabra: ventas, soporte o general.
    
    Mensaje: {state['message']}
    """
    
    result = llm.invoke(llm_prompt)
    intent = result.content.strip().lower()

    print(intent)

    return {
        "intent": intent,
        "steps": ["Crear ficha del cliente"]
    }

def create_draft(state: DraftState) -> dict:
    """
    Create customer draft
    """
    print("Superstep 4: Crear borrador:")
    llm_prompt = f"""
        Eres un asesor comercial. Redacta una respuesta breve, profesional y clara
        para el siguiente mensaje de un cliente, teniendo en cuenta su intención.

        Mensaje del cliente: {state['message']}
        Intención detectada: {state['intent']}

        Responde solo con el borrador de la respuesta, sin explicaciones adicionales.
    """

    draft = llm.invoke(llm_prompt).content.strip()
    print(draft)

    return {
        "draft": draft,
        "steps": ["Generar borrador de respuesta"]
    }

def classify_human_response(answer: str) -> str:
    """
    Quick llm query to classify HITL answer as OK, KO or EDIT
    """
    prompt = f"""
    Un usuario ha respondido a una petición de aprobación de un borrador.
    Clasifica su respuesta en EXACTAMENTE una de estas tres palabras: OK, KO o EDIT

    - "OK" si aprueba o está de acuerdo
    - "KO" si rechaza o no quiere continuar
    - "EDIT" si quiere cambios o correcciones

    Responde ÚNICAMENTE con una palabra: OK, KO o EDIT.

    Respuesta del usuario: "{answer}"
    """
    respuesta = llm.invoke(prompt)
    return respuesta.content.strip()

def human_review(state: DraftState) -> dict:
    """
    Human validation node
    """
    print("Superstep 5: Verificación humana")
    valid_answers = ["OK", "KO", "EDIT"]

    respuesta = interrupt({
        "pregunta": "¿Enviamos este borrador?",
        "borrador": state['draft'],
        "opciones": valid_answers
    })

    human_decision = classify_human_response(respuesta)

    # valid_answers validation
    while human_decision not in valid_answers:
        texto_libre = interrupt({
            "error": "No pude interpretar tu respuesta con claridad",
            "pregunta": "¿Apruebas, rechazas o quieres editar el borrador (solo 5 modificaciones)?",
            "borrador": state["draft"],
        })
        human_decision = classify_human_response(texto_libre)

    return {
        "user_decision": human_decision,
        "steps": [f"Revision humana respondida ({human_decision})"]
    }

def router_human_decision(state: DraftState) -> Literal["OK", "KO", "EDIT"]:
    # validacion de attempts
    if state["user_decision"] == "EDIT" and state["edit_attempts"] >= MAX_EDITION_ATTEMPTS:
        return "KO"
    return state["user_decision"]


def modify_draft(state: DraftState) -> dict:
    """
    Modify draft node
    """
    print("Superstep paralelo 6: Modificar borrador:")

    fixes = interrupt({
        "pregunta": "Escribe las correcciones del borrador",
        "borrador_actual": state["draft"],
    })

    print(f"Correcciones: {fixes}")

    llm_prompt = f"""
        Eres un asesor comercial. El cliente ha dado correcciones sobre el draft que le
        ha sido enviado. Asimila y comprende las correcciones y aplícalas al borrador.
        
        Draft inicial: {state['draft']}
        Correcciones del cliente: {fixes}

        Responde solo con el borrador de la respuesta, sin explicaciones adicionales.
    """
    
    modified_draft = llm.invoke(llm_prompt).content.strip()
    print(f"Draft corregido: \n")
    print(modified_draft)

    tries = state["edit_attempts"] + 1

    return {
        "edit_attempts": tries,
        "draft": modified_draft,
        "steps": [f"Edición número {tries} del borrador."]
    }

def send_draft(state: DraftState) -> dict:
    """
    Send final draft
    """
    print("Superstep paralelo 6: Enviar draft final")
    return {
        "respuesta_final": f"ENVIADO AL CLIENTE: {state['draft']}",
        "steps": [f"Enviado borrador final."]
    }

def end_without_send(state: DraftState) -> dict:
    """
    Draft sending user cancelation
    """
    print("Superstep paralelo 6: Salir sin enviar")
    final_answer = "No se envió respuesta por cancelación del usuario."
    if state["edit_attempts"] >= MAX_EDITION_ATTEMPTS:
        final_answer = "No se envió, exceso de intentos de edición por el usuario." 
    return {
        "respuesta_final": final_answer,
        "steps": [f"Salir sin enviar."]
    }

# Creating graph
workflow = StateGraph(DraftState)

# Creating nodes
workflow.add_node("recibe_customer_message", recibe_customer_message)
workflow.add_node("clasify_user_intent", clasify_user_intent)
workflow.add_node("create_draft", create_draft)
workflow.add_node("human_review", human_review)
workflow.add_node("modify_draft", modify_draft)
workflow.add_node("send_draft", send_draft)
workflow.add_node("end_without_send", end_without_send)

# Creating edges
workflow.add_edge(START, "recibe_customer_message")
workflow.add_edge("recibe_customer_message", "clasify_user_intent")
workflow.add_edge("clasify_user_intent", "create_draft")
workflow.add_edge("create_draft", "human_review")

workflow.add_conditional_edges(
    "human_review",
    router_human_decision,
    {
        "OK": "send_draft",
        "KO": "end_without_send",
        "EDIT": "modify_draft"
    }
)

workflow.add_edge("modify_draft", "human_review")
workflow.add_edge("end_without_send", END)

# Setting up memory and checkpointers
with SqliteSaver.from_conn_string(DB_FILE) as checkpointer:
    hitl_graph = workflow.compile(checkpointer=checkpointer)

    initial_input = {
        "message": USER_PROMPT,
        "edit_attempts": 0,
        "steps": [],
        "thread_id": THREAD_ID
    }

    config = {"configurable": {"thread_id": THREAD_ID}}


    print(""" *****************
    Creando un grafo con Human in the loop
    **************** """)

    print("Superstep 1: START")
    final_exec = hitl_graph.invoke(initial_input, config=config)

    while "__interrupt__" in final_exec:
        pregunta = final_exec["__interrupt__"][0].value
        print("\n--- El grafo necesita tu respuesta ---")
        print(pregunta)

        respuesta_usuario = input("\nTu respuesta: ")

        final_exec = hitl_graph.invoke(
            Command(resume=respuesta_usuario),
            config=config
        )

    print("\n--- Resultado final ---")
    print(final_exec.get("respuesta_final"))
    print("Orden de ejecución:")
    print(final_exec.get("steps"))


    #TODO: Está todo bien pero no funciona la validación de attempts