# Generative AI Lab

This project contains practical Python examples for working with large language models. It focuses on API communication, environment configuration, prompt templates, and secure key management, with Google Gemini as the current provider.

The goal is to provide a clear and reproducible foundation for experimenting with generative AI and understanding how modern model integrations are consumed from code.

## Project overview

This repository includes small examples that demonstrate:

- calling external AI APIs from Python
- configuring credentials through environment variables
- sending prompt-based requests to Gemini
- composing prompts and models with LangChain's runnable pipeline
- keeping configuration separate from application logic

## Stack used

TBD

## Repository structure

```text
.
├── chroma_db/
├── docs/
│   ├── checklist.md
│   ├── notas.txt
│   └── roadmap.md
├── langchain-lab/
│   ├── chatGPT/
│   │   └── main.py
│   └── gemini/
│   │   ├── main.py
│   │   ├── prompt_templates.py
│   │   ├── prompt_templates.txt
│   │   ├── chains.py
│   │   ├── chains.txt
│   │   ├── sequential_chains.py
│   │   ├── sequential_chains.txt
│   │   ├── structured_output.py
│   │   ├── structured_output.txt
│   │   ├── memory.py
│   │   └── memory.txt
├── rag-lab/
│   ├── data/
│   │   ├── jokic_wikipedia.pdf
│   │   ├── lideres_nba_25-26.pdf
│   │   └── season_review_25-26.pdf
│   └── gemini/
│       ├── loaders.py
│       ├── embeddings.py
│       └── embeddings.txt
├── llms-lab/
│   ├── chatGPT/
│   │   ├── main.py
│   │   ├── main.sh
│   │   └── response.txt
│   └── gemini/
│   │   ├── main.py
│   │   ├── main.sh
│   │   └── response.txt
├── README.md
├── .gitignore
├── .env_example
├── CHANGELOG.md
├── LICENSE
└── requirements.txt
```

## Project history and versioning

The project's learning milestones and relevant changes are recorded in the [CHANGELOG](CHANGELOG.md). It uses `0.x` versions while the laboratory is evolving: minor versions represent a new AI concept or integration, and patch versions represent fixes or documentation updates.

## Dependencies

The project dependencies are listed in `requirements.txt`-

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Environment configuration

API keys should never be stored directly in source code. The project uses `python-dotenv` to load credentials from a local `.env` file and keep them out of version control. There is an .env_example on project root.

### Security practices

- Keep `.env` files local and never commit them to GitHub
- Never remove `.env` from `.gitignore`
- Use separate credentials for local development and production
- Rotate keys periodically
- Avoid logging sensitive values or printing tokens in terminal output

There is a .gitignore included on project root.

## Usage

Activate the virtual environment and install the dependencies from the project root:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### LLM

```bash
python llms-lab/chatGPT/main.py > llms-lab/chatGPT/response.txt
python llms-lab/gemini/main.py > llms-lab/gemini/response.txt
```

Added aux curl calls:
```bash
bash llms-lab/chatGPT/main.sh
bash llms-lab/gemini/main.sh
```

### Langchain

```bash
python langchain-lab/chatGPT/main.py > langchain-lab/chatGPT/response.txt
python langchain-lab/gemini/prompt_templates.py > langchain-lab/gemini/prompt_templates.txt
python langchain-lab/gemini/chains.py > langchain-lab/gemini/chains.txt
python langchain-lab/gemini/sequential_chains.py > langchain-lab/gemini/sequential_chains.txt
python langchain-lab/gemini/structured_output.py > langchain-lab/gemini/structured_output.txt
python langchain-lab/gemini/memory.py > langchain-lab/gemini/memory.txt
```

### RAG

```bash
python rag-lab/gemini/embeddings.py > rag-lab/gemini/embeddings.txt
```

## Why this project is relevant

This repository documents a practical progression from direct LLM API calls to reusable LangChain workflows. It records how providers are configured, how models are called from Python, and how increasingly complex AI features are composed step by step while keeping credentials outside the source code.

The project demonstrates:

- Direct integration with OpenAI and Google Gemini APIs.
- Python and shell-based API usage, including `curl` examples.
- Environment-based configuration with `python-dotenv`.
- Secure API-key management through `.env` and `.gitignore`.
- LangChain model wrappers for working with Gemini and OpenAI.
- Reusable prompt templates with single and multiple variables.
- Basic LCEL chains that compose prompts and models with the `|` operator.
- API-enriched chains that add external data to an LLM prompt.
- Sequential chains that pass the output of one model call into another.
- Structured output validated with Pydantic models.
- Conversation memory using message histories and contextual follow-up questions.

Together, these examples establish the fundamentals needed to evolve towards more advanced workflows such as RAG, tool-using agents, and AI-powered backend services.

## Future improvements

The next stage of the roadmap is to apply the LangChain foundations to more advanced AI workflows:

- RAG (Retrieval-Augmented Generation): load documents, split text into chunks, generate embeddings, and store them in a vector database such as ChromaDB.
- Build a complete RAG workflow that answers questions using project-specific documents.
- Experiment with chunking and retrieval strategies to improve response accuracy.
- Build agents with tools and function calling, including workflows that combine multiple tools.
- Expose an AI workflow through a small backend or REST API using FastAPI.
- Add error handling, retries, testing, and deployment-ready configuration patterns.

## Author

elk1o.dev@gmail.com

## License

This project is licensed under the MIT License. Full details are available in the [LICENSE](LICENSE) file included in this repository.

The license governs reuse, modification, and distribution of the code and is documented in the project root for reference.
