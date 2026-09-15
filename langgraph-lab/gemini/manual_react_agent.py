import os
from dotenv import load_dotenv
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
import operator

from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
AISTUDIO_APIKEY = os.getenv('AISTUDIO_APIKEY')
QUESTION = """
Compara el rendimiento de Nikola Jokic en tres contextos distintos: sus estadísticas
en la temporada regular NBA más reciente, su rendimiento con la selección de Serbia
en el último EuroBasket o competición internacional en la que participó, y cuántos
triples-dobles lleva en su carrera NBA hasta la fecha. Con esos tres datos, dame una
valoración de en cuál de los tres contextos ha sido estadísticamente más dominante.
"""

llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        temperature=0,
        google_api_key=AISTUDIO_APIKEY,
        timeout=60,
        max_retries=3,
    )

# Setting up State with persistent memory
class AgentState(TypedDict):

    # setting up the scratchpad
    messages: Annotated[List, operator.add]
    next_action: str
    iterations: int

# Setting up tools
def llm_tool(query: str) -> str:
    print(f"--- Usando herramienta LLM para la consulta {query} ---")
    response = llm.invoke(f"Responde a esta pregunta de forma concisa: {query}")
    return response.content.strip()

# Node definition

# Node 1 - Reasoning
def resasoning_node(state: AgentState):

    print("=== Nodo de razonamiento ===")

    # Setting up infinite loop prevention
    if state['iterations'] >= 5:
        print ("--- Agente: Se ha alcanzado el límite de iteraciones. Finalizando ejecución ---")
        return {"next_action": "END"}

    # Retrieving history of messages
    history = "\n".join(state["messages"])

    # Setting up react agent prompt. We order 1 think 2 decide an action (tool or END)
    prompt = f"""
        Eres un agente de IA que responde a la pregunta: "{state['messages'][0]}"
        La conversación hasta ahora es:
        {history}

        Reglas OBLIGATORIAS:
            1. Cada Action debe pedir SOLO UN dato concreto por vez, nunca varios a la vez.
            2. Si la pregunta original tiene varios datos que obtener, identifica cuántos
            faltan revisando el historial de Observations anteriores, y pide solo
            el SIGUIENTE dato que falte, uno por uno.
            3. NUNCA formules una Action que combine "y" para pedir más de un dato

        ¿Necesitas usar una herramienta para obtener más información o ya tienes suficiente para responder?
        Si necesitas mas información, responde ÚNICAMENTE con:
            Thought: [Tu razonamiento sobre que información necesitas].
            Action: [La pregunta específica para la herramienta].

        Si crees que ya tienes suficiente infromación para dar una respuesta final, responde ÚNICAMENTE con:
            Thought: [Tu razonamiento de por qué ya tienes suficiente información].
            Action: END.
    """

    # 1 Think.
    response = llm.invoke(prompt)
    decision = response.content.strip()
    print(f"Decisión del LLM: {decision}")

    # 2 Decide. Updating State with LLM's THOUGHT/ACTION response. Next_action is key.
    if "Action: END" in decision:
        # Only return modified fields, langgraph will update State only with this fields
        return {"messages": [decision], "next_action": "END"} 
    else:
        # Only return modified fields, langgraph will update State only with this fields
        return {"messages": [decision], "next_action": "Action"} 

# Node 2 - Action 
def action_node(state: AgentState):
    """
    The "action" node. It runs if the reasoning node decides to use a tool.
    It parses the action from the last message, calls the tool, and returns the result
    as an "OBSERVATION".
    """
    print("=== Nodo de acción ===")

    # 1 - Parse
    last_thought = state["messages"][-1]

    try:
        # Extracting the tool query (text after ACTION:)
        query = last_thought.split("Action:")[1].strip()
    except IndexError:
        # Handle the error if the LLM does not format the output correctly
        return {
            "messages": ["Observation: No se ha podido parsear la acción. Recuerda responder con el formato 'Action: [tu pregunta]'."],
            "iterations": state["iterations"]+1
        }

    # 2 - Run
    result = llm_tool(query)

    print(f"Observation: {result}")

    # 3 - Consider. Returning result as an "observation"
    return {
        "messages": [f"Observation: {result}"],
        "iterations": state["iterations"]+1
    }

def generate_answer_node(state: AgentState):
    """
    Final node. It runs when brain decides Action: END.
    Resume the entire history (Question, Thought, Action, and Observations)
    in a clean final answer.
    """
    print("=== Nodo de respuesta final ===")
    history = "\n".join(state["messages"])

    prompt = f"""
        Basado en el siguiente historial de conversación (preguntas, pensamientos, 
        acciones y observaciones), redacta uan respuesta final completa, clara y bien estructurada
        para la pregunta inicial del usuario.

        Historial: {history}

        Respuesta final para el usuario:
    """

    final_answer = llm.invoke(prompt)
    # Last message will be final answer
    return {"messages": [final_answer.content.strip()]}

print("""
*****************
Creando un grafo de un agente react con LangGraph
****************
""")

# Creating langgraph workflow with AgentState dict as its template
workflow = StateGraph(AgentState)

# Adding nodes to workflow
workflow.add_node("think",resasoning_node)
workflow.add_node("action",action_node)
workflow.add_node("answer",generate_answer_node)

# Setting up as first node to execute
workflow.set_entry_point("think")
# Setting up edges

def should_continue(state: AgentState):
    """
    Main router function. Decide next step based on next_action field
    """
    if state.get("next_action") == "END":
        return "end" # Go final answer node
    else:
        return "continue" # Go action node

workflow.add_conditional_edges(
    "think", # Source node
    should_continue, # Decision function according to return
    {
        "continue": "action",
        "end": "answer",
    }
)

# Edge between action - think
workflow.add_edge("action", "think")

# Edge between answer - END
workflow.add_edge("answer", END)

app = workflow.compile()
print("Grafo compilado, listo para ejecutar")

initial_state = {
    "messages": [f"Pregunta del usuario {QUESTION}"],
    "iterations": 0,
    "next_action": ""
}

print(f'\n\n --- Iniciando agente con la pregunta: "{QUESTION}" ---')

final_state = None

# Using stream to see each step of exec
for s in app.stream(initial_state, {"recursion_limit": 15}):
    print(s)
    print("------")
    final_state = s # Saving last status to print last answer

# Printing last answer
print("--- Ejecución finalizada ---")
print("Respuesta final del agente: ")
if final_state:
    print(next(iter(final_state.values()))["messages"][-1])
else:
    print("No se pudo obtener el estado final")
