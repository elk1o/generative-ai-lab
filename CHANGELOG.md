# Changelog

Todos los cambios relevantes de este proyecto se documentan en este archivo.

El proyecto sigue una versión educativa de [Semantic Versioning](https://semver.org/):

- `MAJOR`: cambio de enfoque o reorganización incompatible del laboratorio.
- `MINOR`: nuevo concepto, integración o ejemplo funcional.
- `PATCH`: corrección, ajuste de configuración o mejora documental.

## [Unreleased]

### Planned

- Continuar el recorrido por RAG y agentes según el roadmap.

## [0.7.0] - Conversation memory

### Added

- Ejemplo de memoria conversacional en `langchain-lab/gemini/memory.py`.
- Historial compartido de mensajes mediante una lista de `HumanMessage` y `AIMessage`.
- Función `call_AI_with_history` que conserva el contexto y lo envía al modelo en cada interacción.
- Demostración de recuperación de información proporcionada en un mensaje anterior.
- Guardado de la salida del ejemplo en `langchain-lab/gemini/memory.txt`.

## [0.6.0] - Structured LangChain output

### Added

- Ejemplo de salida estructurada en `langchain-lab/gemini/structured_output.py`.
- Definición del modelo Pydantic `Player` para describir los datos esperados.
- Uso de `ChatPromptTemplate.from_template` para crear el prompt.
- Uso de `with_structured_output(Player)` para recibir un objeto Python validado en lugar de texto libre.
- Comprobación del tipo de resultado devuelto por la cadena.
- Guardado de la salida del ejemplo en `langchain-lab/gemini/structured_output.txt`.

## [0.5.0] - Sequential LangChain chains

### Added

- Ejemplo de cadena secuencial en `langchain-lab/gemini/sequential_chains.py`.
- Composición LCEL de una primera cadena de estadísticas y una segunda cadena de análisis.
- Uso de `RunnablePassthrough.assign` para pasar automáticamente el resultado de la primera cadena a la segunda.
- Uso de `StrOutputParser` para convertir las respuestas del modelo en texto antes de encadenarlas.
- Guardado de la salida del ejemplo en `langchain-lab/gemini/sequential_chains.txt`.

## [0.4.0] - API-enriched LangChain chain

### Added

- `langchain-lab/gemini/chains.py`.
- Consulta de jugadores en la API externa Ball Don't Lie.
- Enriquecimiento de un prompt de Gemini con los datos devueltos por la API.
- Composición de `PromptTemplate` y `ChatGoogleGenerativeAI` mediante LCEL (`prompt_template | llm`).
- Ejecución de la cadena con `chain.invoke(...)` y presentación del análisis generado.

## [0.3.0] - Basic LangChain chains

### Added

- Primeros ejemplos de LangChain con Gemini y OpenAI.
- Uso de modelos mediante wrappers de LangChain.
- Uso de `PromptTemplate` para separar la plantilla del prompt de la lógica de ejecución.
- Cadenas básicas que conectan prompt y modelo mediante LCEL.

## [0.2.0] - Direct LLM API calls

### Added

- Primeras llamadas directas a las APIs de OpenAI y Gemini.
- Ejemplos de ejecución desde Python en `llms-lab/`.
- Scripts auxiliares de `curl` para probar las APIs desde shell.
- Ficheros de respuesta para conservar ejemplos de salida.

## [0.1.0] - Project foundation

### Added

- Estructura inicial del laboratorio de IA generativa.
- Entorno virtual de Python y dependencias base en `requirements.txt`.
- Configuración de credenciales mediante variables de entorno y `python-dotenv`.
- Documentación inicial, roadmap y checklist de aprendizaje.
- Configuración inicial de Git y publicación del proyecto.
