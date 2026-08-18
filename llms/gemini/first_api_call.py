from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
AISTUDIO_APIKEY = os.getenv('AISTUDIO_APIKEY')
PROMPT = "¿Puedes decirme que agente de IA eres? Es mi primera llamada remota de API de la IA"

print("*************************")
print("Starting firt Gemini api call script")
print(f"Question: {PROMPT}")

client = genai.Client(api_key=AISTUDIO_APIKEY)

try:
    interaction = client.interactions.create(
        model="gemini-3.7-flash",
        input=PROMPT
    )
    print(f"Answer: {interaction.output_text}");

except Exception as e:
    print(f"\n Error detectado: \n {e}")


print("")
print("Ending first api call script")
print("***********************")