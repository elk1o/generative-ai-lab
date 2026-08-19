from dotenv import load_dotenv
import os
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

# 1 - Prompttemplate basic variable

prompt_template_single_var = PromptTemplate.from_template("El mejor jugador de baloncesto del mundo es {jugador}")
print(prompt_template_single_var.format(jugador="Nikola Jokic"))

# 2 - Prompttemplate multiple variables

template = "El mejor jugador de baloncesto del mundo es {jugador} y juega en el equipo {equipo} de la liga {liga}"
prompt_template_multiple_var = PromptTemplate.from_template(template)
print(prompt_template_multiple_var.format(jugador="Nikola Jokic", equipo="Denver Nuggets", liga="NBA"))

# 3 - Prompttemplate + OpenAI call
try:
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=OPENAI_API_KEY)
    ia_prompt = "Eres un experto en estadísticas de baloncesto y necesito que saques los puntos por partido que promedió {jugador} en la pasada temporada"
    prompt_template_ia = PromptTemplate(
        input_variables=["jugador"],
        template=ia_prompt
    )

    chain = LLMChain(llm=llm, prompt=prompt_template_ia)
    ia_response = chain.run(jugador="Nikola Jokic")
    print(ia_response)

except Exception as e:
    if "credit_balance_exhausted" in str(e) or "429" in str(e):
        print("\n Error: No tienes créditos en tu cuenta de OpenAI")
    else:
        print(f"\n Error detectado: {e}")