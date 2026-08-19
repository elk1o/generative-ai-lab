from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
AISTUDIO_APIKEY = os.getenv('AISTUDIO_APIKEY')
PROMPT = "¿Puedes decirme que agente de IA eres? Es mi primera llamada remota de API de la IA"

print("*************************")
print("Starting firt Gemini api call script")
print(f"Question: {PROMPT}")

try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0,
        google_api_key=AISTUDIO_APIKEY
    )

    response = llm.invoke(PROMPT)
    print(f"Answer: {response.content}")

except Exception as e:
    print(f"\n Error detectado: \n {e}")

print("")
print("Ending first api call script")
print("***********************")