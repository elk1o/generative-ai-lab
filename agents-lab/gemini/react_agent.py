from dotenv import load_dotenv
import os, wikipedia, time
from langchain.prompts import PromptTemplate
from langchain import hub
from langchain.agents import Tool, AgentExecutor, initialize_agent, create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_experimental.tools import PythonREPLTool
from langchain_google_genai import ChatGoogleGenerativeAI
from agent_template import REACT_AGENT_PROMPT

load_dotenv()
AISTUDIO_APIKEY = os.getenv('AISTUDIO_APIKEY')
TEMPLATE = '''
    Responde las siguientes preguntas en español lo mejor que puedas.
    Preguntas: {q}
'''
GOAL_QUESTIONS = [
    "Tell me about Nikola Jokic",
    "What country was the last FIFA WC champions?",
    "Tell me the first 50 of fibonacci sequence"
]
prompt_template = PromptTemplate.from_template(TEMPLATE)
prompt = REACT_AGENT_PROMPT

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0,
    google_api_key=AISTUDIO_APIKEY,
    timeout=60,
    max_retries=3,
)

# Adding tools
# Tool 1: Python exec support
python_repl = PythonREPLTool()
python_repl_tool = Tool(
    name="Python REPL",
    func=python_repl.run,
    description="Útil cuando necesitas usar Python para responder preguntas. Debes introducir código Python"
)


# Tool 2: Wikipedia search support
# Setting up headers to avoid API blocks
wikipedia.set_user_agent("MiAgenteIA/1.0 (elk1o.dev@gmail.com)")
wikipedia.set_lang("en")  # O "es" según la versión de Wikipedia que prefieras
# Setting up limits on Wrapper
wiki_wrapper = WikipediaAPIWrapper(
    top_k_results=1,
    doc_content_chars_max=1000
)
wikipedia = WikipediaQueryRun(api_wrapper=wiki_wrapper)
wikipedia_tool = Tool(
    name="Wikipedia",
    func=wikipedia.run,
    description="Útil cuando necesites buscar información sobre un tema, país, persona etc en Wikipedia"
)

# Tool 3: DDG search support
ddg = DuckDuckGoSearchRun()
ddg_tool = Tool(
    name="Duckduckgo search",
    func=ddg.run,
    description="Útil cuando necesites buscar información en internet para encontrar información que otra herramienta no puede proporcionar."
)

# List of tools
agent_tools = [python_repl_tool, wikipedia_tool, ddg_tool]

# Creating agent
agent = create_react_agent(llm, agent_tools, prompt)

print("*****************")
print(f"Creating ReAct agent")
print("*****************")

agent_executor = AgentExecutor(
    agent=agent,
    tools=agent_tools,
    verbose=False,
    handle_parsing_errors=True,
    max_iterations=5
)

for i, question in enumerate(GOAL_QUESTIONS, start=1):

    try:
        print(f"Question {i}: {question}:")
        output = agent_executor.invoke({
            "input": prompt_template.format(q=question)
        })
        print(f"Answer {i}: {output['output']}")
        print()
        time.sleep(15) # Time sleep to avoid reach RPM limit on aistudio apikey

    except Exception as e:
            print(f"ERROR: Error procesando la pregunta {i}: {e}")