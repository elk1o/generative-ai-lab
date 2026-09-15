import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
AISTUDIO_APIKEY = os.getenv('AISTUDIO_APIKEY')
CONTEXT = """
    El equipo de baloncesto Denver Nuggets el campeonato en 2023. Su jugador franquicia, Nikola Jokic, anotó el tiro decisivo en la final.
"""
QUESTION = """
    ¿Quien anotó la canasta decisiva?
"""

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0,
    google_api_key=AISTUDIO_APIKEY,
    timeout=60,
    max_retries=3,
)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente útil. Responde a la pregunta basada únicamente en el contexto proporcionado"),
    ("user", "{context} \n\nPregunta: {question}")
])

# Setting up llm output to string
output_parser = StrOutputParser()

chain = prompt_template | llm | output_parser 

respuesta = chain.invoke({
    "context": CONTEXT,
    "question": QUESTION
})

print("*****************")
print(f"Creating basic chain with langchain")
print("*****************")

print(f"Pregunta: {QUESTION}")
print(f"Respuesta: {respuesta}")