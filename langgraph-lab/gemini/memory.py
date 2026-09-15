import operator
import os
import argparse
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.checkpoint.sqlite import SqliteSaver
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END, START

load_dotenv()
AISTUDIO_APIKEY = os.getenv('AISTUDIO_APIKEY')
DB_FILE = os.getenv('DB_FILE')

# Get the sent parameters in execution
parser = argparse.ArgumentParser(description="Agente de seguimiento comercial con memoria persistente")
parser.add_argument("user_prompt", type=str, help="Mensaje del cliente")
parser.add_argument("thread_id", type=str, help="Identificador único del cliente/sesión")
args = parser.parse_args()
user_prompt = args.user_prompt
thread_id = args.thread_id

llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        temperature=0,
        google_api_key=AISTUDIO_APIKEY,
        timeout=60,
        max_retries=3,
    )

# Setting up State
class CustomerProfileState(TypedDict):
    message: str
    clean_message: str
    short_message: str
    keywords: List[str]
    urgency: str
    profile: str
    thread_id: str
    # setting up the scratchpad to record nodes exec order
    steps: Annotated[List[str], operator.add]
    history: Annotated[list[str], operator.add]

# 2 - Setup nodes functions
def recibe_customer_message(state: CustomerProfileState) -> dict:
    """
    Setting up user prompt
    """
    print("Superstep 2: Mensaje de input de usuario:")
    print(user_prompt)
    print(f"Recibido thread_id interno: {thread_id}")
    return {
        "thread_id": thread_id,
        "steps":["Recibir mensaje de usuario y settear thread_id"]
    }

def clean_user_message(state: CustomerProfileState) -> dict:
    """
    Cleaning up user prompt
    """
    clean_msg = " ".join(state["message"].strip().split())
    print("Superstep 3: Limpiar mensaje:")
    print(clean_msg)
    return {
        "clean_message": clean_msg,
        "steps": ["Limpiar mensaje de usuario"]
    }

def summary_user_message(state: CustomerProfileState) -> dict:
    """
    Chopping user prompt to 
    """
    llm_prompt = f"Te mando un texto de un cliente, necesito que lo resumas a 90 caracteres y le añadas '...'. Devuelve solo el texto resumido. Texto: {state['clean_message']}"
    response = llm.invoke(llm_prompt)

    print("Superstep 4 en paralelo: Resumir mensaje:")
    print(response.content.strip())

    return{
        "short_message": response.content.strip(),
        "steps": ["Acortar el mensaje a 90 caracteres"]
    }

def extract_keywords(state: CustomerProfileState) -> dict:
    llm_prompt = f"Te mando un texto de un cliente, necesito que extraigas las entidades de negocio relevantes mencionadas en este mensaje (temas como precio, demo, soporte, producto, facturación. Saca solo las palabras clave separadas entre comas.). Texto: {state['clean_message']}"
    response = llm.invoke(llm_prompt)

    print("Superstep 4 en paralelo: Extraer palabras clave")
    print(response.content.strip())

    keywords = [
        keyword.strip() for keyword in response.content.strip().split(",") if keyword.strip()
    ]

    return{
        "keywords": keywords,
        "steps": ["Extraer palabras clave"]
    }

def setup_urgency(state: CustomerProfileState) -> dict:
    llm_prompt = f"Te mando un texto de un cliente, necesito que identifiques el nivel de urgencia que tiene el cliente para la tarea que solicita. Devuelve el nivel de urgencia en una palabra. Texto: {state['clean_message']}"
    response = llm.invoke(llm_prompt)

    print("Superstep 4 en paralelo: Determinar urgencia")
    print(response.content.strip())

    return{
        "urgency": response.content.strip(),
        "steps": ["Determinar urgencia"]
    }

def check_user_history(state: CustomerProfileState) -> dict:
    """
    Not necessary with the current logic; included for scalability.
    """
    print("Superstep 5: Comprobar si existe historial")
    previous_history = state.get("history")
    
    if previous_history:
        print(f"Historial encontrado para este thread_id: {previous_history}")
    else:
        print("Historial previo no encontrado")
    
    return {
        "steps": ["Comprobar historial del cliente"]
    }

def create_customer_profile(state: CustomerProfileState) -> dict:

    previous_history = state.get("history", [])

    if previous_history:
        to_string_history = "Historial previo del cliente:\n" + "\n".join(
            f"- {msg}" for msg in previous_history
        )
    else:
        to_string_history = "No hay interacciones previas registradas."

    llm_prompt = ChatPromptTemplate.from_template("""
        Eres un asistente que prepara fichas de contexto para agentes comerciales.
        Con la siguiente información, redacta una ficha clara y legible en texto plano, 
        con saltos de línea entre cada sección. Ten en cuenta el historial si existe.

        Mensaje: {message}
        Resumen del mensaje: {short_message}
        Palabras clave detectadas: {keywords}
        Urgencia detectada: {urgency}
        Historial: {to_string_history}
    """)

    chain = llm_prompt | llm | StrOutputParser()
    
    result = chain.invoke({
        "message": state["message"],
        "short_message": state["short_message"],
        "keywords": ", ".join(state["keywords"]),
        "urgency": state["urgency"],
        "to_string_history": to_string_history,
    })

    print("Superstep 6: Crear ficha de usuario en función de los siguientes datos:")
    print(f"""
        - Mensaje: {state['message']}
        - Resumen del mensaje: {state['short_message']}
        - Palabras clave detectadas: {', '.join(state['keywords'])}
        - Urgencia detectada: {state['urgency']}
        - Historial: {to_string_history}
    """)
    print(result)

    return {
        "profile": result,
        "steps": ["Crear ficha del cliente"],
        "history": [state["message"]]
    }

# 3 - Setup graph
workflow = StateGraph(CustomerProfileState)

workflow.add_node("recibe_customer_message",recibe_customer_message)
workflow.add_node("clean_user_message", clean_user_message)
workflow.add_node("summary_user_message", summary_user_message)
workflow.add_node("extract_keywords", extract_keywords)
workflow.add_node("setup_urgency", setup_urgency)
workflow.add_node("check_user_history", check_user_history)
workflow.add_node("create_customer_profile", create_customer_profile)

workflow.add_edge(START, "recibe_customer_message")
workflow.add_edge("recibe_customer_message", "clean_user_message")

# Fan-out
workflow.add_edge("clean_user_message", "summary_user_message")
workflow.add_edge("clean_user_message", "extract_keywords")
workflow.add_edge("clean_user_message", "setup_urgency")
# Fan-in
workflow.add_edge(["summary_user_message","extract_keywords","setup_urgency"],"check_user_history")

workflow.add_edge("check_user_history", "create_customer_profile")
workflow.add_edge("create_customer_profile", END)

# Setting up memory and checkpointers
with SqliteSaver.from_conn_string(DB_FILE) as checkpointer:
    memory_graph = workflow.compile(checkpointer=checkpointer)

    print("""
    *****************
    Creando un grafo fan-out fan-in en Langgraph con memoria
    ****************
    """)
    
    resultado = memory_graph.invoke(
        {"message": user_prompt},
        {"configurable": {"thread_id": thread_id}}
    )
