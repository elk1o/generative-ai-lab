from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()
AISTUDIO_APIKEY = os.getenv('AISTUDIO_APIKEY')
SYSTEM_CONTEXT = """
    Eres un experto en estadísticas de baloncesto de la NBA. Recuerda que mi jugador favorito es Nikola Jokic que juega en los Denver Nuggets."
"""

llm = ChatGoogleGenerativeAI(
    model="gemini-3.7-flash",
    temperature=0,
    google_api_key=AISTUDIO_APIKEY
)

history = []

def call_AI_with_history(user_input):
    # In modern LangChain, "memory" is simply a list of messages
    # passed to the model each time. HumanMessage - AIMessage - HumanMessage - AIMessage
    history.append(HumanMessage(content=user_input))
    response = llm.invoke(history)
    history.append(AIMessage(content=response.content))
    return response.content

def call_AI_with_system_context(user_input, SYSTEM_CONTEXT):
    historial = [SystemMessage(content=SYSTEM_CONTEXT)]
    response = llm.invoke(historial + [HumanMessage(content=user_input)])
    return response.content

print("*****************")
print("Gemini calls with memory. Second call should remember the first one")
print("*****************")
print("First call: my favourite player is Nikola Jokic who plays for the Denver Nuggets")
print(call_AI_with_history("Me jugador favorito es Nikola Jokic que juega en los Denver Nuggets"))
print("")
print("Second call: ¿Who is my favourite player?")
print(call_AI_with_history("¿Cúal es mi jugador favorito?"))  # Check if remembers


print("*****************")
print("Gemini calls with preset system context memory.")
print("*****************")
print(f"Context: {SYSTEM_CONTEXT}")
print("")
print("Calling AI: Who are you and what is my favourite player?")
print (call_AI_with_system_context("¿Quien eres y cúal es mi jugador favorito?", SYSTEM_CONTEXT))