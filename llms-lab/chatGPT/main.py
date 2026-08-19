from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_APIKEY = os.getenv('OPENAI_API_KEY')
PROMPT = "¿Puedes decirme que agente de IA eres? Es mi primera llamada remota de API de la IA"

print("*************************")
print("Starting firt ChatGPT api call script")
print(f"Question: {PROMPT}")

client = OpenAI(api_key=OPENAI_APIKEY)

try:
  response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {"role": "user", "content": PROMPT}
    ],
    store=True,
  )
  print(f"Answer: {response.choices[0].message.content}")

except Exception as e:
    print(f"\n Error detectado: \n {e}")

print("")
print("Ending first api call script")
print("***********************")