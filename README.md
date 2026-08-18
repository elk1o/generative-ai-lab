# LLM API Integration

This project contains a set of practical examples for integrating Python applications with large language model APIs. The repository focuses on API communication, environment configuration, and secure key management, using OpenAI and Google Gemini as reference providers.

The goal is to build a base clear and reproducible foundation for experimenting with LLMs and understanding how modern AI services are consumed from code.

## Project overview

This repository includes small examples that demonstrate:

- calling external AI APIs from Python
- configuring credentials through environment variables
- sending prompt-based requests to different providers
- testing API responses with shell scripts and curl
- keeping configuration separate from application logic

## Stack used

- Python 3.14
- OpenAI API
- Google Gemini API
- python-dotenv
- pip and dependency management

check requirements.txt for aditional info.

## Repository structure

```text
.
├── .env_example
├── requirements.txt
├── llms/
│   ├── chatGPT/
│   │   ├── first_api_call.py
│   │   ├── first_api_call_curl.sh
│   │   └── response.txt
│   └── gemini/
│       ├── first_api_call.py
│       ├── first_api_call_curl.sh
│       └── response.txt
├── README.md
```

## Dependencies

The project dependencies are listed in `requirements.txt`:

- `openai` — Python client for OpenAI APIs
- `google-genai` — Python client for Google Gemini APIs
- `python-dotenv` — loads environment variables from a `.env` file
- `ipython` — interactive Python environment

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Environment configuration

API keys should never be stored directly in source code. The project uses `python-dotenv` to load credentials from a local `.env` file and keep them out of version control.

### Example `.env`

```env
OPENAI_API_KEY=your_openai_api_key_here
AISTUDIO_APIKEY=your_gemini_api_key_here
```

### Security practices

- keep `.env` files local and never commit them to GitHub
- add `.env` to `.gitignore`
- use separate credentials for local development and production
- rotate keys periodically
- avoid logging sensitive values or printing tokens in terminal output

Example `.gitignore`:

```gitignore
.env
__pycache__/
*.pyc
```
or check project gitignore.

## Usage

Run the Python example:

```bash
python llms/chatGPT/first_api_call.py > llm/chatGPT/response.txt
python llms/gemini/first_api_call.py > llm/gemini/response.txt
```

Run the curl example:

```bash
bash llms/chatGPT/first_api_call_curl.sh
bash llms/gemini/first_api_call_curl.sh
```

## Why this project is relevant

This repository reflects a practical, hands-on approach to AI integration. It demonstrates the type of work often required when building AI-powered tools and services, including secure configuration, API consumption, and experimentation with prompt-driven workflows.

It is a useful project for showing foundational knowledge in:

- LLM integration
- Python automation
- external API usage
- configuration management
- secure development practices

## Future improvements

This project can be extended with:

- a small web interface using Flask or FastAPI
- conversation flows with memory
- a multi-provider abstraction layer
- prompt templates and structured responses
- error handling and retries
- deployment-ready configuration patterns

## Author

elk1o.dev@gmail.com

## License

This project is licensed under the MIT License. Full details are available in the [LICENSE](LICENSE) file included in this repository.

The license governs reuse, modification, and distribution of the code and is documented in the project root for reference.
