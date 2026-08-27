"""
Agente de briefing semanal — Calendario + Tiempo + Búsqueda web
Combina tres herramientas para generar un briefing completo semanal
"""
import os
import datetime
import requests
from dotenv import load_dotenv

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.prompts import PromptTemplate
from agent_template import AGENT_PROMPT

load_dotenv()
AISTUDIO_APIKEY = os.getenv('AISTUDIO_APIKEY')
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
LATITUDE = 40.4168
LONGITUDE = -3.7038
CITY = "Madrid"
GOAL_QUESTION = """
    Consulta mi Google Calendar y el tiempo previsto para esta semana.
    Cruza ambas informaciones para avisarme de posibles conflictos
    (eventos presenciales con mal tiempo).
    Si hay reuniones con temas o empresas concretas que merezca la pena
    investigar, busca contexto relevante.
    Termina con prioridades claras y un consejo para arrancar bien la semana.
"""

# Google calendar auth
def get_calendar_service():
    """Autentica y devuelve el servicio de Google Calendar."""
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


# Tool 1: Google calendar
def get_week_events(_: str = "") -> str:
    """Obtiene todos los eventos de TODOS los calendarios desde hoy hasta el domingo."""
    service = get_calendar_service()

    today = datetime.datetime.now(datetime.timezone.utc)
    days_until_sunday = (6 - today.weekday()) % 7 or 7
    end_of_week = today + datetime.timedelta(days=days_until_sunday)

    time_min = today.isoformat()
    time_max = end_of_week.replace(hour=23, minute=59, second=59).isoformat()

    dias_es = {
        0: "lunes", 1: "martes", 2: "miércoles", 3: "jueves",
        4: "viernes", 5: "sábado", 6: "domingo"
    }
    dia_actual = dias_es[today.weekday()]

    calendar_list = service.calendarList().list().execute()
    calendarios = calendar_list.get("items", [])

    all_events = []
    for cal in calendarios:
        cal_id = cal["id"]
        cal_name = cal.get("summary", cal_id)

        events_result = service.events().list(
            calendarId=cal_id,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy="startTime",
            maxResults=250,
        ).execute()

        eventos_cal = events_result.get("items", [])
        for event in eventos_cal:
            event["_calendario_origen"] = cal_name
        all_events.extend(eventos_cal)

    # Cabecera que indica el rango real de fechas — así el LLM sabe
    # si es un briefing de semana completa o de días restantes
    if today.weekday() == 0:
        output = f"EVENTOS DE LA SEMANA (hoy {dia_actual}, semana completa):\n\n"
    else:
        output = f"EVENTOS RESTANTES DE LA SEMANA (hoy {dia_actual}, hasta el domingo):\n\n"

    if not all_events:
        return output + "No hay eventos en este rango."

    def get_sort_key(event):
        return event["start"].get("dateTime", event["start"].get("date", ""))

    all_events.sort(key=get_sort_key)

    current_day = None
    for event in all_events:
        start = event["start"].get("dateTime", event["start"].get("date", ""))

        if "T" in start:
            dt = datetime.datetime.fromisoformat(start.replace("Z", "+00:00"))
            day_label = dt.strftime("%A %d/%m")
            time_label = dt.strftime("%H:%M")
        else:
            dt = datetime.datetime.fromisoformat(start)
            day_label = dt.strftime("%A %d/%m")
            time_label = "Todo el día"

        if day_label != current_day:
            output += f"\n Day {day_label.upper()}\n"
            current_day = day_label

        title = event.get("summary", "Sin título")
        location = event.get("location", "")
        origen = event.get("_calendario_origen", "")

        output += f"  • {time_label} — {title} [{origen}]"
        if location:
            output += f" Ubicación {location}"
        output += "\n"

    return output

# Tool 2: weather (open-meteo API)
def consultar_tiempo(ciudad: str = CITY) -> str:
    """
    Consulta la previsión del tiempo para los próximos 7 días.
    Usa Open-Meteo, una API gratuita que no requiere API key.
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={LATITUDE}&longitude={LONGITUDE}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max"
        f"&timezone=Europe/Madrid"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        return f"Error al consultar el tiempo: {e}"

    resultado = f"PREVISIÓN DEL TIEMPO EN {ciudad.upper()}:\n\n"
    for i, fecha in enumerate(data["daily"]["time"]):
        max_temp = data["daily"]["temperature_2m_max"][i]
        min_temp = data["daily"]["temperature_2m_min"][i]
        lluvia = data["daily"]["precipitation_probability_max"][i]

        dt = datetime.datetime.fromisoformat(fecha)
        dia_semana = dt.strftime("%A %d/%m")

        aviso_lluvia = "Posible lluvia" if lluvia >= 50 else ""
        resultado += f"  {dia_semana}: {min_temp}°C - {max_temp}°C, {lluvia}% prob. lluvia{aviso_lluvia}\n"

    return resultado

# Tool 3: Web search (duckduckgo)
search = DuckDuckGoSearchRun()

def search_context(query) -> str:
    """Busca contexto o noticias recientes sobre un tema, persona o empresa."""
    return search.run(query)

# Tool definition
tools = [
    Tool(
        name="consultar_calendario",
        func=get_week_events,
        description=(
            "Consulta Google Calendar y devuelve todos los eventos de la semana actual. "
            "Úsala siempre al principio para saber qué hay en el calendario. "
            "No necesita ningún input — pasa una cadena vacía."
        ),
    ),
    Tool(
        name="consultar_tiempo",
        func=consultar_tiempo,
        description=(
            "Consulta la previsión del tiempo para los próximos 7 días en una ciudad. "
            "Úsala para saber si va a llover o hacer buen/mal tiempo en los días con eventos. "
            "Input: nombre de la ciudad (opcional, por defecto Madrid)."
        ),
    ),
    Tool(
        name="buscar_contexto",
        func=search_context,
        description=(
            "Busca información o noticias recientes sobre un tema, persona o empresa. "
            "Úsala para enriquecer el contexto de reuniones o eventos importantes. "
            "Input: una query de búsqueda concreta en español o inglés."
        ),
    ),
]

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0.3,
    google_api_key=AISTUDIO_APIKEY,
    timeout=60,
    max_retries=3,
)

print("*****************")
print(f"Creating ReAct agent with custom tools (Google calendar, open meteo)")
print("*****************")

agent = create_react_agent(llm, tools, AGENT_PROMPT)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=False,
    max_iterations=5,
    handle_parsing_errors=True
)

# script exec
if __name__ == "__main__":
    print("Generando tu briefing semanal...\n")
    output = agent_executor.invoke({"input": GOAL_QUESTION})
    print("="*60)
    print(output["output"])