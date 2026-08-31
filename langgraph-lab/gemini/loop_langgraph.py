import os
from dotenv import load_dotenv
from typing import TypedDict
from langgraph.graph import StateGraph, END

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
AISTUDIO_APIKEY = os.getenv('AISTUDIO_APIKEY')
QUESTION = """
    ¿Como está el tiempo hoy?
"""

class AgentState(TypedDict):
    question: str
    answer: str
    attempts: int

# Node 1 - llm query
def generate_answer(state: AgentState):

    print(f"Agente: Generando respuesta.. Intento {state['attempts'] + 1}")

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        temperature=0,
        google_api_key=AISTUDIO_APIKEY,
        timeout=60,
        max_retries=3,
    )

    prompt_template = ChatPromptTemplate.from_template(
        """
        Responde a la siguiente pregunta {question}. \n
        Por favor, se educado y asegúrate de incluir la palabra gracias en tu respuesta.
        """
    )

    # LCEL chain
    chain = prompt_template | llm | StrOutputParser()

    respuesta = chain.invoke({
        "question": state['question']
    })

    return {
        "answer": respuesta,
        "attempts": state["attempts"] + 1
    }

# Node 2 - Determining if answer is valid
def determine_next_step(state: AgentState):
    answer = state["answer"]
    print(f"Agente: Revisando respuesta: {answer}")

    if "NHL" in answer.lower():
        print("Agente: Respuesta validada. Habla sobre la NHL (Liga nacional de hockey)")
        return "OK"
    else:
        print("Agente: Respuesta rechazada. No habla sobre la NHL (Liga nacional de hockey)")

        if state["attempts"] >= 3:
            print("Agente: Demasiados intentos fallidos. Finalizando ejecución sin éxito.")
            return "KO"
        else:
            print("Agente: Reconsultando...")
            return "RETRY"
# Creating langgraph workflow with AgentState dict as its template
workflow = StateGraph(AgentState)
# Adding node 1 to workflow
workflow.add_node("query",generate_answer)
# Setting up as first node to execute
workflow.set_entry_point("query")
# Setting up edges
workflow.add_conditional_edges(
    "query", # Source node
    determine_next_step, # Decision function according to return
    {
        "OK": END,
        "KO": END,
        "RETRY": "query"
    }
)
# Freezing graph structure in an Runnable object
app = workflow.compile()

print("*****************")
print(f"Creando un grafo recursivo con LangGraph")
print("*****************")

inputs = {
    "question": QUESTION,
    "attempts": 0,
    "answer": ""
}

# Using stream to see each step of exec
for s in app.stream(inputs, {"recursion_limit": 5}):
    print(s)
    print("------")