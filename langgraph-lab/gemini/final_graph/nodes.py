from langgraph.prebuilt import create_react_agent
from state import FinalDraftState
from constants import USER_PROMPT, LLM, MAX_DRAFT_EDITION_ATTEMPTS, MAX_ASK_EDITION_ATTEMPTS
from langgraph.types import interrupt
from tools import search_AI_training, calculate_budget

def recibe_customer_message(state: FinalDraftState) -> dict:
    """
    Setting up user prompt
    """
    print("Superstep 2: Mensaje de input de usuario:")
    print(USER_PROMPT)
    return {
        "log":["Recibir mensaje de usuario"]
    }

def clasify_user_intent(state: FinalDraftState) -> dict:
    """
    Clasify user intent by message
    """
    print("Superstep 3: Clasificar la intención del usuario:")

    llm_prompt = f"""
    Clasifica la intención del siguiente mensaje de un cliente en EXACTAMENTE una de estas categorías: ventas, soporte, general
    
    - "ventas" si pregunta por precios, planes, demos, compras o cotizaciones
    - "soporte" si reporta un problema, error, o algo que no funciona
    - "general" si no encaja claramente en las anteriores
    
    Responde ÚNICAMENTE con una palabra: ventas, soporte o general.
    
    Mensaje: {state['message']}
    """
    
    result = LLM.invoke(llm_prompt)
    intent = result.text.strip().lower()
    if intent not in {"ventas", "soporte", "general"}:
        intent = "general"
    print(f"Departamento: {intent}")
    return {
        "intent": intent,
        "log": ["Clasificar intención del cliente"]
    }

def send_soporte_answer(state: FinalDraftState) -> dict:
    """
    Answer soporte draft
    """
    print("Superstep paralelo 3: Dar repuesta del departamento de soporte")
    answer = "Bienvenido al departamento de soporte. Para cualquier consulta contáctanos al correo soporte@soporte.com"
    print(answer)

    return {
        "respuesta_final": answer,
        "log": ["Respuesta del departamento de soporte"]
    }

def send_informacion_general_answer(state: FinalDraftState) -> dict:
    """
    Answer información general draft
    """
    print("Superstep paralelo 3: Dar repuesta del departamento de información general")
    answer = "Bienvenido al departamento de información general. Para cualquier consulta contáctanos al correo info@info.com"
    print(answer)
    
    return {
        "respuesta_final": answer,
        "log": ["Respuesta del departamento de información general"]
    }

def classify_human_response(answer: str, with_edit: bool) -> str:
    """
    Quick llm query to classify HITL answer as OK, KO or EDIT if applies
    """
    if with_edit:
        prompt = f"""
        Un usuario ha respondido a una petición de aprobación de un borrador.
        Clasifica su respuesta en EXACTAMENTE una de estas tres palabras: OK, KO o EDIT

        - "OK" si aprueba, está de acuerdo o quiere continuar
        - "KO" si rechaza, no quiere continuar o quiere salir
        - "EDIT" si quiere cambios o correcciones

        Responde ÚNICAMENTE con una palabra: OK, KO o EDIT.

        Respuesta del usuario: "{answer}"
        """
    else:
        prompt = f"""
        Un usuario ha respondido a una petición de aprobación de un borrador.
        Clasifica su respuesta en EXACTAMENTE una de estas tres palabras: OK o KO

        - "OK" si aprueba o está de acuerdo
        - "KO" si rechaza o quiere modificar la pregunta

        Responde ÚNICAMENTE con una palabra: OK o KO

        Respuesta del usuario: "{answer}"
        """
    
    respuesta = LLM.invoke(prompt)
    return respuesta.text.strip().upper()

def validate_initial_data(state: FinalDraftState) -> dict:
    """
    Validate initial prompt data
    """
    print("Superstep paralelo 3: Verificación del prompt inicial")

    respuesta = interrupt({
        "question": "¿Quieres enviar esta consulta o prefieres modificarla?",
        "message": state["message"]
    })

    initial_data_decision = classify_human_response(respuesta, with_edit=False)

    return {
        "initial_data_user_decision": initial_data_decision,
        "log": ["Validar consulta inicial"]
    }

def modify_initial_data(state: FinalDraftState) -> dict:
    """
    Modify initial prompt data
    """
    print("Superstep paralelo 4: Modificar consulta inicial:")

    remaining_tries = MAX_ASK_EDITION_ATTEMPTS - (state["initial_data_tries"] + 1)
    new_initial_prompt = interrupt({
        "pregunta": f"Escribe de nuevo la consulta (Modificaciones restantes: {remaining_tries})",
        "consulta_actual": state["message"],
    })

    print(f"Nueva consulta: {new_initial_prompt}")

    tries = state["initial_data_tries"] + 1

    return {
        "initial_data_tries": tries,
        "message": new_initial_prompt,
        "log": [f"Edición número {tries} de la consulta inicial."]
    }

def setup_analysis(state: FinalDraftState) -> dict:
    """
    Initial node made only to fan-out next superstep
    """
    print("Superstep paralelo 4: Preparar análisis")
    return {
        "log": ["Preparando análisis"]
    }

def setup_urgency(state: FinalDraftState) -> dict:
    """
    Node for setting up urgency based on initial prompt
    """
    print("Superstep 5 en paralelo: Determinar urgencia")
    llm_prompt = f"Te mando un texto de un cliente, necesito que identifiques el nivel de urgencia que tiene el cliente para la tarea que solicita. Devuelve el nivel de urgencia en una palabra. Texto: {state['message']}"
    response = LLM.invoke(llm_prompt)

    print(response.text.strip())

    return {
        "urgency": response.text.strip(),
        "log": ["Determinar urgencia"]
    }

def extract_keywords(state: FinalDraftState) -> dict:
    """
    Node to extract keywords from user prompt
    """
    print("Superstep 5 en paralelo: Extraer palabras clave")
    llm_prompt = f"Te mando un texto de un cliente, necesito que extraigas las entidades de negocio relevantes mencionadas en este mensaje (temas como precio, demo, soporte, producto, facturación. Saca solo las palabras clave separadas entre comas.). Texto: {state['message']}"
    response = LLM.invoke(llm_prompt)

    print(response.text.strip())

    keywords = [
        keyword.strip() for keyword in response.text.strip().split(",") if keyword.strip()
    ]

    return {
        "keywords": keywords,
        "log": ["Extraer palabras clave"]
    }

def summary_user_message(state: FinalDraftState) -> dict:
    """
    Chopping user prompt to 
    """
    print("Superstep 5 en paralelo: Resumir mensaje:")
    llm_prompt = f"Te mando un texto de un cliente, necesito que lo resumas a 90 caracteres y le añadas '...'. Devuelve solo el texto resumido. Texto: {state['message']}"
    response = LLM.invoke(llm_prompt)

    print(response.text.strip())

    return {
        "short_message": response.text.strip(),
        "log": ["Acortar el mensaje a 90 caracteres"]
    }

def generate_AI_draft(state: FinalDraftState) -> dict:
    """
    Generate draft with AI Agent enrichment
    """
    print("Superstep 6: Crear borrador con agente IA")

    agent = create_react_agent(
        model=LLM,
        tools=[
            search_AI_training,
            calculate_budget
        ],
        prompt=(
            "Eres un asesor comercial B2B especializado en formación corporativa de IA. "
            "Debes usar las herramientas disponibles para buscar el programa más adecuado y calcular un presupuesto referencial. "
            "Responde en español, con tono profesional, claro y breve. "
            "No digas que el presupuesto es definitivo; indícala como referencial y sujeta a validación comercial."
        )
    )
    respuesta_agente = agent.invoke({
            "messages": [(
                    "user",
                    "Genera un borrador de respuesta comercial para este caso. "
                    "Usa las herramientas para buscar un programa y calcular una cotización referencial.\n\n"
                    f"Mensaje del cliente: {state['message']}\n"
                    f"Resumen: {state['short_message']}\n"
                    f"Palabras clave: {', '.join(state['keywords'])}\n"
                    f"Urgencia: {state['urgency']}"
                )]
            },
        config={"recursion_limit": 15}
    )
    ultimo_mensaje = respuesta_agente["messages"][-1]
    # El .content de Gemini 3 puede venir como lista de bloques; .text lo normaliza si existe.
    draft = ultimo_mensaje.text if hasattr(ultimo_mensaje, "text") else ultimo_mensaje.content
    if isinstance(draft, list):
        draft = " ".join(
            bloque.get("text", "") if isinstance(bloque, dict) else str(bloque)
            for bloque in draft
        )
    print("Borrador generado por el agente:")
    print(draft)
    return {
        "draft": draft,
        "log": ["Generar borrador con agente IA"]
    }

def validate_draft(state: FinalDraftState) -> dict:
    """
    Validate initial prompt data
    """
    print("Superstep 7: Verificación del borrador")

    respuesta = interrupt({
        "question": "¿Quieres enviar este borrador, prefieres modificarlo o salir sin enviar?",
        "borrador": state["draft"]
    })

    draft_user_decision = classify_human_response(answer=respuesta, with_edit=True)

    return {
        "draft_user_decision": draft_user_decision,
        "log": ["Validar borrador"]
    }

def send_draft(state: FinalDraftState) -> dict:
    """
    Send final draft
    """
    print("Superstep paralelo 8: Enviar draft final")
    return {
        "respuesta_final": f"ENVIADO AL CLIENTE: {state['draft']}",
        "log": [f"Enviado borrador final."]
    }

def end_without_send(state: FinalDraftState) -> dict:
    """
    Draft sending user cancelation
    """
    print("Superstep paralelo 8: Salir sin enviar")
    final_answer = "No se envió respuesta por cancelación del usuario."
    if state["draft_edit_tries"] >= MAX_DRAFT_EDITION_ATTEMPTS:
        final_answer = "No se envió, exceso de intentos de edición por el usuario." 
    return {
        "respuesta_final": final_answer,
        "log": [f"Salir sin enviar."]
    }

def modify_draft(state: FinalDraftState) -> dict:
    """
    Modify draft node
    """
    print("Superstep paralelo 6: Modificar borrador:")

    remaining_corrections = MAX_DRAFT_EDITION_ATTEMPTS - (state["draft_edit_tries"] + 1)
    fixes = interrupt({
        "pregunta": f"Escribe las correcciones del borrador (Correcciones restantes: {remaining_corrections})",
        "borrador_actual": state["draft"],
    })

    print(f"Correcciones: {fixes}")

    llm_prompt = f"""
        Eres un asesor comercial. El cliente ha dado correcciones sobre el draft que le
        ha sido enviado. Asimila y comprende las correcciones y aplícalas al borrador.
        
        Draft inicial: {state['draft']}
        Correcciones del cliente: {fixes}

        Responde solo con el borrador de la respuesta, sin explicaciones adicionales.
    """
    
    modified_draft = LLM.invoke(llm_prompt).text.strip()
    print(f"Borrador corregido: \n")
    print(modified_draft)

    tries = state["draft_edit_tries"] + 1

    return {
        "draft_edit_tries": tries,
        "draft": modified_draft,
        "log": [f"Edición número {tries} del borrador."]
    }