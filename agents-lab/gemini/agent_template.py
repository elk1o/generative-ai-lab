from langchain_core.prompts import PromptTemplate

REACT_AGENT_PROMPT = PromptTemplate.from_template("""
Responde a la siguiente pregunta lo mejor que puedas. Tienes acceso a las siguientes herramientas:

{tools}

REGLA IMPORTANTE: Nunca respondas desde tu conocimiento propio sin verificar.
Si la respuesta no viene directamente de una herramienta, usa SIEMPRE
'buscar_contexto' para verificar antes de contestar cualquier dato factual.

Usa el siguiente formato:

Question: la pregunta de entrada que debes responder
Thought: siempre debes pensar qué hacer
Action: la acción a tomar, debe ser una de [{tool_names}]
Action Input: la entrada para la acción
Observation: el resultado de la acción
... (este ciclo Thought/Action/Action Input/Observation puede repetirse N veces)
Thought: ya sé la respuesta final
Final Answer: la respuesta final a la pregunta original

Begin!

Question: {input}
Thought: {agent_scratchpad}
""")

