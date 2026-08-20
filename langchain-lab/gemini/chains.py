from dotenv import load_dotenv
import os

load_dotenv()
AISTUDIO_APIKEY = os.getenv('AISTUDIO_APIKEY')
BDL_APIKEY = os.getenv('BALL_DONT_LIE_APIKEY')
PLAYER = "Jokic"

import requests
from datetime import date
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

BASE_URL = "https://api.balldontlie.io"

headers = {"Authorization": BDL_APIKEY}

response = requests.get(
    f"{BASE_URL}/v1/players",
    headers=headers,
    params={"search": PLAYER}
)

bdl_player_raw_data = response.json()

if bdl_player_raw_data['data']:
    player_data = bdl_player_raw_data['data'][0]

    # Call the Google Generative AI model with prompttemplate with enriched API data

    template = """
        Eres un experto en estadísticas de baloncesto y análisis de rendimiento de jugadores. A continuación, se te proporcionan los datos de un jugador específico. Tu tarea es entender los datos que se te aportan a continuación y generar un resumen conciso y detallado del jugador, incluyendo cualquier información relevante que pueda ser útil para dar a conocer al jugador. Asegúrate de que el resumen sea claro, informativo y fácil de entender:
        {player_data}
    """

    prompt_template = PromptTemplate(
        input_variables=["player_data"],
        template=template
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0,
        google_api_key=AISTUDIO_APIKEY
    )

    chain = prompt_template | llm

    print("*****************")
    print(f"Consulting the basketball expert analyst about the given player's data '{PLAYER}'")
    print("*****************")
    print("")
    print(chain.invoke({"player_data": player_data}).content)

else:
    print(f'Not found player "{PLAYER}".')