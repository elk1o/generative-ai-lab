# Changelog

All relevant changes to this project are documented in this file.

The project follows an educational version of [Semantic Versioning](https://semver.org/):

- `MAJOR`: a change in direction or an incompatible reorganization of the lab.
- `MINOR`: a new concept, integration, or functional example.
- `PATCH`: a bug fix, configuration adjustment, or documentation improvement.

## [0.11.1] - Security guardrails

### Added

- Use of security guardrails to make AI workflows safer and more controlled.
- Input and output constraints to reduce unsafe, irrelevant, or unexpected model behavior.

## [0.11.0] - ReAct agent with tools

### Added

- ReAct agent in `react_agent.py` using Gemini and LangChain.
- Custom ReAct prompt template in `react_agent_template.py`.
- Python REPL tool for executing Python code when needed.
- Wikipedia tool for querying information about people, countries, and topics.
- DuckDuckGo search tool for retrieving information from the internet.
- `AgentExecutor` configuration with verbose execution, parsing error handling, and a maximum of five iterations.
- Example questions covering general knowledge, current information, and Fibonacci sequence generation.
- Output saved to `agents-lab/gemini/react_agent.txt`.

## [0.10.0] - Multi-source RAG

### Added

- A RAG workflow capable of working with information from multiple PDF documents.
- `multiple_sources_loaders.py` to load and prepare multiple document sources.
- `multiple_sources_embeddings.py` to generate embeddings and persist them in a dedicated ChromaDB collection.
- `multiple_sources_final_rag.py` to retrieve combined context from multiple sources and generate a response with Gemini.
- Use of `source` metadata to identify the original document for each retrieved chunk.
- Multi-source similarity search and display of the retrieved chunks before running the RAG chain.
- Questions that combine information from different documents into a single answer.
- Output files `multiple_sources_embeddings.txt` and `multiple_sources_final_rag.txt`.

## [0.9.0] - Complete RAG workflow

### Added

- Complete RAG example in `rag-lab/gemini/final_rag.py`.
- Loading of the existing ChromaDB vector database without re-indexing the documents.
- Similarity search to retrieve the most relevant chunks.
- Use of a retriever to provide document context to the model.
- Complete RAG chain with `ChatPromptTemplate`, `RunnablePassthrough`, and `StrOutputParser`.
- A prompt that requires the model to answer only with information from the retrieved context.
- Output saved to `rag-lab/gemini/final_rag.txt`.

## [0.8.0] - RAG loaders and embeddings

### Added

- Initial RAG components in `rag-lab/gemini/`.
- `loaders.py` to load PDF documents with `PyPDFLoader`.
- Document splitting into chunks using `RecursiveCharacterTextSplitter`.
- `embeddings.py` to convert chunks into vectors with `GoogleGenerativeAIEmbeddings`.
- Persistence of embeddings and documents in ChromaDB.
- Basic validation of the collection and indexed chunks.
- `chroma_db/` directory to store the local vector database.

## [0.7.0] - Conversation memory

### Added

- Conversation memory example in `langchain-lab/gemini/memory.py`.
- Shared message history using a list of `HumanMessage` and `AIMessage` objects.
- `call_AI_with_history` function that preserves the context and sends it to the model on each interaction.
- Demonstration of retrieving information provided in a previous message.
- Output saved to `langchain-lab/gemini/memory.txt`.

## [0.6.0] - Structured LangChain output

### Added

- Structured output example in `langchain-lab/gemini/structured_output.py`.
- Definition of the Pydantic `Player` model to describe the expected data.
- Use of `ChatPromptTemplate.from_template` to create the prompt.
- Use of `with_structured_output(Player)` to receive a validated Python object instead of free-form text.
- Checking the type of result returned by the chain.
- Output saved to `langchain-lab/gemini/structured_output.txt`.

## [0.5.0] - Sequential LangChain chains

### Added

- Sequential chain example in `langchain-lab/gemini/sequential_chains.py`.
- LCEL composition of a first statistics chain and a second analysis chain.
- Use of `RunnablePassthrough.assign` to automatically pass the first chain's result to the second.
- Use of `StrOutputParser` to convert model responses to text before chaining them.
- Output saved to `langchain-lab/gemini/sequential_chains.txt`.

## [0.4.0] - API-enriched LangChain chain

### Added

- `langchain-lab/gemini/chains.py`.
- Player lookup through the external Ball Don't Lie API.
- Enrichment of a Gemini prompt with the data returned by the API.
- Composition of `PromptTemplate` and `ChatGoogleGenerativeAI` using LCEL (`prompt_template | llm`).
- Execution of the chain with `chain.invoke(...)` and display of the generated analysis.

## [0.3.0] - Basic LangChain chains

### Added

- First LangChain examples with Gemini and OpenAI.
- Use of models through LangChain wrappers.
- Use of `PromptTemplate` to separate the prompt template from the execution logic.
- Basic chains connecting prompts and models through LCEL.

## [0.2.0] - Direct LLM API calls

### Added

- First direct calls to the OpenAI and Gemini APIs.
- Python execution examples in `llms-lab/`.
- Auxiliary `curl` scripts for testing the APIs from the shell.
- Response files to preserve example outputs.

## [0.1.0] - Project foundation

### Added

- Initial structure of the generative AI lab.
- Python virtual environment and base dependencies in `requirements.txt`.
- Credential configuration through environment variables and `python-dotenv`.
- Initial documentation, roadmap, and learning checklist.
- Initial Git configuration and project publication.
