import os
from dotenv import load_dotenv

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from langchain.agents import AgentExecutor, Tool, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
AISTUDIO_APIKEY = os.getenv('AISTUDIO_APIKEY')

# Alcance necesario para interactuar con Assistant
SCOPES = ['https://www.googleapis.com/auth/assistant-sdk-prototype']

# 1. Función para manejar la autenticación OAuth2 y enviar el comando
def ejecutar_comando_asistente(comando_texto: str) -> str:
    creds = None
    # Si ya te autenticaste antes, reutiliza el token guardado
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # Si no hay token válido, abre el navegador para autorizar la app
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Envío del texto al motor de Google Assistant 
    print(f"\n📡 [Google Assistant SDK] Enviando orden: '{comando_texto}'")
    # Nota: Aquí la API ejecuta la instrucción en tu ecosistema domótico
    return f"Éxito: Se envió el comando '{comando_texto}' a Google Home."

# 2. Encapsular la función en una Tool de LangChain[cite: 3]
assistant_tool = Tool(
    name="GoogleHomeControl",
    func=ejecutar_comando_asistente,
    description="Útil para enviar órdenes de voz/texto en lenguaje natural a los dispositivos de Google Home (ej: 'enciende la luz del salón')."
)

# 3. Inicializar el LLM y el agente ReAct[cite: 3]
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("AISTUDIO_APIKEY")[cite: 1, 3]
)

tools = [assistant_tool]

template = """Responde a la solicitud decidiendo qué comandos enviar a la casa.

Herramientas disponibles:
{tools}

Formato estricto a seguir:
Question: la instrucción recibida
Thought: piensa qué orden concreta de Google Home se necesita
Action: la herramienta a usar, debe ser una de [{tool_names}]
Action Input: la instrucción textual exacta para el asistente (ej. "Enciende la luz del salón")
Observation: el resultado de la acción
Thought: ya he completado la tarea
Final Answer: la confirmación al usuario

Begin!

Question: {input}
Thought: {agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)
agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)[cite: 3]
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)[cite: 3]

# 4. Prueba de ejecución
if __name__ == "__main__":
    orden = "Voy a ponerme a trabajar en el escritorio, prepara la habitación."
    agent_executor.invoke({"input": orden})[cite: 3]