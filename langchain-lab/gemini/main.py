from dotenv import load_dotenv
import os

load_dotenv()
AISTUDIO_APIKEY = os.getenv('AISTUDIO_APIKEY')

from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

#Prompttemplate basic variable

prompt_template_single_var = PromptTemplate.from_template("El mejor jugador de baloncesto del mundo es {jugador}")

print("*****************")
print("First string concat with prompt templates, multiple variables")
print("*****************")
print(prompt_template_single_var.format(jugador="Nikola Jokic"))
print("")

#Prompttemplate multiple variables

template = (
    "El mejor jugador de baloncesto del mundo es {jugador} y juega en el equipo "
    "{equipo} de la liga {liga}"
)
prompt_template_multiple_var = PromptTemplate.from_template(template)
print("*****************")
print("Second string concat with prompt templates, multiple variables")
print("*****************")
print(
    prompt_template_multiple_var.format(
        jugador="Nikola Jokic",
        equipo="Denver Nuggets",
        liga="NBA"
    )
)
print("")

# 3 - Prompttemplate + Gemini call

try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0,
        google_api_key=AISTUDIO_APIKEY
    )

    ia_prompt = (
        "Eres un experto en estadísticas de baloncesto y necesito que saques "
        "los puntos por partido que promedió {jugador} en la pasada temporada."
    )

    prompt_template_ia = PromptTemplate(
        input_variables=["jugador"],
        template=ia_prompt
    )

    chain = prompt_template_ia | llm
    ia_response = chain.invoke({"jugador": "Nikola Jokic"})

    print("*****************")
    print("Third string concat with prompt templates, enriched by Gemini call")
    print("*****************")

    print(ia_response.content)

except Exception as e:
    print(f"\n Error detectado: {e}")