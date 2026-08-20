from dotenv import load_dotenv
import os

load_dotenv()
AISTUDIO_APIKEY = os.getenv('AISTUDIO_APIKEY')
PLAYER = "Nikola Jokic"
TEMPORADA = "2025-2026"

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
# Call the Google Generative AI model with prompttemplate with enriched API data

player_stats_prompt = """
    Eres un experto en estadísticas de baloncesto de la NBA. Saca las estadísticas del jugador {PLAYER} de la temporada {TEMPORADA}. Sin conclusiones ni análisis, solo proporciona las estadísticas de la temporada solicitada. Asegúrate de que las estadísticas sean precisas y estén actualizadas.
"""

basket_expert_prompt = """
    Eres un experto analista de baloncesto. Teniendo en cuenta estas estadísticas {player_stats} del jugador {PLAYER} de la temporada {TEMPORADA} de la NBA de este jugador, haz un análisis detallado de su desempeño en esa temporada. Asegúrate de que el análisis sea profesional, claro, informativo y fácil de entender. Además, proporciona una estimación del salario que podría recibir en su nuevo contrato basado en su desempeño y estadísticas.
"""

stats_expert_prompt_template = PromptTemplate(
    template=player_stats_prompt,
    input_variables=["PLAYER", "TEMPORADA"],
)

stats_llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0,
    google_api_key=AISTUDIO_APIKEY
)

# Having player statistics, consulting basketball expert for analysis and salary estimation
basketball_llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0,
    google_api_key=AISTUDIO_APIKEY
)

basketball_expert_prompt_template = PromptTemplate(
    template=basket_expert_prompt,
    input_variables=["player_stats", "TEMPORADA", "PLAYER"]
)

# The first chain's output becomes the input of the second chain.
stats_chain = stats_expert_prompt_template | stats_llm | StrOutputParser()
sequential_chain = (
    RunnablePassthrough.assign(
        player_stats=stats_chain
    )
    | basketball_expert_prompt_template
    | basketball_llm
    | StrOutputParser()
)

print("*****************")
print(f"Analyzing by the basketball expert economic situation of player '{PLAYER}'")
print("*****************")
print("")
print(sequential_chain.invoke({
    "TEMPORADA": TEMPORADA,
    "PLAYER": PLAYER
}))

## In this example, the stats that first prompt retrieve are from 2023-2024 season. This is because how LLMs work. They are trained with data until a certain date, and they don't have access to real-time data or data until specific dates. The output reflects that the 2025-2026 season has not yet ocurred. So, when you ask for stats from 2025-2026, the model will provide information based on its training data, which may not include the most recent season's stats.

## In next steps, we will train with RAG to fix this issue, and we will be able to retrieve the real stats from 2025-2026 season.