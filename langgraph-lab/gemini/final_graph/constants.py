import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import uuid

load_dotenv()
AISTUDIO_APIKEY = os.getenv('AISTUDIO_APIKEY')
DB_FILE = os.getenv('DB_FILE')
THREAD_ID = f"client-final-{uuid.uuid4().hex[:8]}"
USER_PROMPT = """
    Hola, queremos una formación de IA básica para 25 personas. ¿Nos pueden dar presupuesto?
"""
MAX_DRAFT_EDITION_ATTEMPTS = 2
MAX_ASK_EDITION_ATTEMPTS = 2
COURSES_CATALOGUE = {
    "basico": {"nombre": "IA para equipos - Nivel Básico", "precio_por_persona": 150, "duracion_horas": 8},
    "intermedio": {"nombre": "IA para equipos - Nivel Intermedio", "precio_por_persona": 250, "duracion_horas": 16},
    "avanzado": {"nombre": "IA aplicada - Nivel Avanzado", "precio_por_persona": 400, "duracion_horas": 24},
}

LLM = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        temperature=0,
        google_api_key=AISTUDIO_APIKEY,
        timeout=60,
        max_retries=3,
    )
