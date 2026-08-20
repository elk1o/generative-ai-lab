from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()
AISTUDIO_APIKEY = os.getenv('AISTUDIO_APIKEY')
PLAYER = "Nikola Jokic"

# Defining the output structure
class Player(BaseModel):
    name: str = Field(description="Nombre")
    position: str = Field(description="Posición en el campo")
    height: str = Field(description="Altura")
    weight: str = Field(description="Peso")
    jersey_number: int = Field(description="Dorsal")
    team: str = Field(description="Equipo")

# More efficient way to make prompt templates
player_data_prompt = ChatPromptTemplate.from_template(
    "Dame los datos del jugador {PLAYER}."
)

# Calling LLM with structured output
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0,
    google_api_key=AISTUDIO_APIKEY
)

structured_output_llm = llm.with_structured_output(Player)
chain = player_data_prompt | structured_output_llm
resultado = chain.invoke({"PLAYER": PLAYER})

print("*****************")
print(f"Consulting specific data player {PLAYER} with specific and structured output")
print("*****************")
print(resultado)
print("")
print("*****************")
print("Type of data returned by the structured output chain")
print("*****************")
print(type(resultado))