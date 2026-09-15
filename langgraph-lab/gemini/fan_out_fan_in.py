import operator
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END, START

load_dotenv()
AISTUDIO_APIKEY = os.getenv('AISTUDIO_APIKEY')
USER_PROMPT = """
    Hola, necesito una demo del producto y saber el precio de la licencia. Es urgente para hoy.
"""

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
    profile: dict
    answer: str
    # setting up the scratchpad to record nodes exec order
    steps: Annotated[List[str], operator.add]

def recibe_customer_message(state: CustomerProfileState) -> dict:
    """
    Setting up user prompt
    """
    print("Superstep 2: Mensaje de input de usuario:")
    print(USER_PROMPT)
    return {
        "steps":["Recibir mensaje de usuario"]
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

    return{
        "keywords": response.content.strip(),
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

def create_customer_profile(state: CustomerProfileState) -> dict:
    llm_prompt = ChatPromptTemplate.from_template("""
        Eres un asistente que prepara fichas de contexto para agentes comerciales.
        Con la siguiente información, redacta una ficha clara y legible en texto plano, 
        con saltos de línea entre cada sección:

        Mensaje: {message}
        Resumen del mensaje: {short_message}
        Palabras clave detectadas: {keywords}
        Urgencia detectada: {urgency}
    """)

    chain = llm_prompt | llm | StrOutputParser()
    
    result = chain.invoke({
        "message": state["message"],
        "short_message": state["short_message"],
        "keywords": ", ".join(state["keywords"]),
        "urgency": state["urgency"],
    })

    print("Superstep 5: Crear ficha de usuario")
    print(result)

    return {
        "profile": result,
        "steps": ["Crear ficha del cliente"]
    }

# Creating graph
workflow = StateGraph(CustomerProfileState)

# Creating nodes
workflow.add_node("recibe_customer_message", recibe_customer_message)
workflow.add_node("clean_user_message", clean_user_message)
workflow.add_node("summary_user_message", summary_user_message)
workflow.add_node("extract_keywords", extract_keywords)
workflow.add_node("setup_urgency", setup_urgency)
workflow.add_node("create_customer_profile", create_customer_profile)

# Creating edges
workflow.add_edge(START, "recibe_customer_message")
workflow.add_edge("recibe_customer_message", "clean_user_message")

# Fan-out
workflow.add_edge("clean_user_message", "summary_user_message")
workflow.add_edge("clean_user_message", "extract_keywords")
workflow.add_edge("clean_user_message", "setup_urgency")

# Fan-in (another way)
workflow.add_edge(
    ["summary_user_message","extract_keywords","setup_urgency"], 
    "create_customer_profile"
)

workflow.add_edge("create_customer_profile", END)

final_workflow = workflow.compile()

initial_input = {
    "message": USER_PROMPT,
    "steps": []
}

print("""
*****************
Creando un grafo fan-out fan-in en Langgraph con llamadas LLM para enriquecer la información
****************
""")
print("Superstep 1: START")
final_result = final_workflow.invoke(initial_input)
print("Superstep final: END")
print("Orden de ejecución:")
print(final_result["steps"])