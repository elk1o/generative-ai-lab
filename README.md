# Generative AI Lab

Generative AI Lab is a collection of practical Python examples that build from direct LLM API calls to complete retrieval, agent, and graph-based workflows. The lab uses OpenAI and Google Gemini, with LangChain, ChromaDB, and LangGraph for orchestration.

Version `1.0.0` marks the first complete release of the lab. Each folder is a standalone learning example; generated `.txt` files preserve selected sample outputs.

## What is included

- Direct calls to OpenAI and Gemini APIs from Python and shell scripts.
- LangChain prompt templates, LCEL chains, sequential workflows, structured output, and conversation history.
- RAG workflows over PDF documents, including a multi-document ChromaDB collection.
- Tool-using ReAct agents, including Google Calendar, weather, web search, Wikipedia, and Python examples.
- LangGraph loops, conditional routing, fan-out/fan-in, human review, and SQLite-backed checkpoints.
- A complete LangGraph customer-response workflow with intent routing, parallel analysis, a tool-using agent, and human approval/edit steps.

## Technology

Python, LangChain, LangGraph, Google Gemini, OpenAI, ChromaDB, Pydantic, SQLite, `python-dotenv`, Google Calendar API, and HTTP APIs. The supported dependency ranges are listed in [requirements.txt](requirements.txt).

## Repository structure

This tree lists the files tracked in the repository. Local credentials, virtual environments, generated databases, caches, and ignored documentation are not included.

```text
.
├── agents-lab/
│   └── gemini/
│       ├── custom_tools/
│       │   ├── agent_template.py
│       │   ├── custom_tools_agent.py
│       │   └── custom_tools_agent.txt
│       └── multitools/
│           ├── agent_template.py
│           ├── react_agent.py
│           ├── react_agent.txt
│           └── react_agent_verbose.txt
├── langchain-lab/
│   ├── chatGPT/
│   │   └── main.py
│   └── gemini/
│       ├── chains.py
│       ├── chains.txt
│       ├── memory.py
│       ├── memory.txt
│       ├── prompt_templates.py
│       ├── prompt_templates.txt
│       ├── sequential_chains.py
│       ├── sequential_chains.txt
│       ├── structured_output.py
│       └── structured_output.txt
├── langgraph-lab/
│   └── gemini/
│       ├── basic_langchain.py
│       ├── fan_out_fan_in.py
│       ├── fan_out_fan_in.txt
│       ├── final_graph/
│       │   ├── constants.py
│       │   ├── graph.png
│       │   ├── graph.py
│       │   ├── main.py
│       │   ├── nodes.py
│       │   ├── state.py
│       │   └── tools.py
│       ├── human_in_the_loop.py
│       ├── loop_langgraph.py
│       ├── loop_langgraph.txt
│       ├── manual_react_agent.py
│       ├── manual_react_agent.txt
│       ├── memory.py
│       ├── memory_exec_1.txt
│       ├── memory_exec_2.txt
│       └── memory_exec_3.txt
├── llms-lab/
│   ├── chatGPT/
│   │   ├── main.py
│   │   ├── main.sh
│   │   └── response.txt
│   └── gemini/
│       ├── main.py
│       ├── main.sh
│       └── response.txt
├── rag-lab/
│   ├── data/
│   │   ├── jokic_wikipedia.pdf
│   │   ├── lideres_nba_25-26.pdf
│   │   ├── season_review_25-26.pdf
│   │   └── triples_dobles_sports_illustrated.pdf
│   └── gemini/
│       ├── embeddings.py
│       ├── embeddings.txt
│       ├── final_rag.py
│       ├── final_rag.txt
│       ├── loaders.py
│       ├── multiple_sources_embeddings.py
│       ├── multiple_sources_embeddings.txt
│       ├── multiple_sources_final_rag.py
│       ├── multiple_sources_final_rag.txt
│       └── multiple_sources_loaders.py
├── .env_example
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── README.md
└── requirements.txt
```

## Getting started

Use Python 3.10 or newer, then create and activate a virtual environment from the repository root and install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with `.venv\Scripts\Activate.ps1`.

Copy `.env_example` to `.env` and replace the placeholders with credentials for the examples you plan to run. The examples load environment variables with `python-dotenv`; do not commit `.env`, API keys, OAuth credentials, or generated token files.

Common settings in `.env_example` include:

- `AISTUDIO_APIKEY` for Gemini examples.
- `OPENAI_API_KEY` for OpenAI examples.
- `BALL_DONT_LIE_APIKEY` for the Ball Don't Lie API example.
- `RAG_DATA_PATH`, `SQLITE_DISK_DIRECTORY`, `COLLECTION_NAME`, `MULTIPLE_SOURCES_COLLECTION_NAME`, and `CHROMADB_EMBEDDINGS_MODEL` for RAG examples.
- `DB_FILE` for LangGraph SQLite checkpoints.

The OpenAI shell wrapper reads `OPENAI_APIKEY`; set it to the same value as `OPENAI_API_KEY` in `.env` when running `llms-lab/chatGPT/main.sh`.

The custom-tools Google Calendar example also requires a Google OAuth client file named `credentials.json` in the repository root. It creates `token.json` during authorization. Both files contain credentials and must remain local.

## Running examples

Run commands from the repository root after setting up the environment. LLM-backed examples require network access and may incur provider API charges.

### LLM API calls

```bash
python llms-lab/chatGPT/main.py
python llms-lab/gemini/main.py
bash llms-lab/chatGPT/main.sh
bash llms-lab/gemini/main.sh
```

### LangChain

```bash
python langchain-lab/chatGPT/main.py
python langchain-lab/gemini/prompt_templates.py
python langchain-lab/gemini/chains.py
python langchain-lab/gemini/sequential_chains.py
python langchain-lab/gemini/structured_output.py
python langchain-lab/gemini/memory.py
```

### RAG

The embedding examples index the included PDFs in ChromaDB. Run an indexing example before its corresponding RAG query example.

```bash
python rag-lab/gemini/embeddings.py
python rag-lab/gemini/final_rag.py
python rag-lab/gemini/multiple_sources_embeddings.py
python rag-lab/gemini/multiple_sources_final_rag.py
```

### Agents

The custom-tools example uses Google Calendar OAuth in addition to the Gemini key.

```bash
python agents-lab/gemini/multitools/react_agent.py
python agents-lab/gemini/custom_tools/custom_tools_agent.py
```

### LangGraph

The human-in-the-loop and complete-graph examples are interactive and wait for responses in the terminal. Reuse the same thread ID in the memory example to continue a conversation across runs.

```bash
python langgraph-lab/gemini/loop_langgraph.py
python langgraph-lab/gemini/manual_react_agent.py
python langgraph-lab/gemini/fan_out_fan_in.py
python langgraph-lab/gemini/human_in_the_loop.py
python langgraph-lab/gemini/memory.py "What plans do you offer?" "client-1"
python langgraph-lab/gemini/memory.py "Can you remind me what I asked?" "client-1"
python langgraph-lab/gemini/final_graph/main.py
```

The complete graph writes its rendered diagram to `graph.png` in the current working directory. LangGraph checkpoint databases and ChromaDB data are local runtime artifacts.

## Project status and versioning

The learning lab is complete at version `1.0.0`. The examples and release history are documented in the [CHANGELOG](CHANGELOG.md). The changelog records the earlier `0.x` milestones and the first complete `1.0.0` release.

## Author

elk1o.dev@gmail.com

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
