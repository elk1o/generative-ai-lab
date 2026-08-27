import os
# Evita conflictos de Protobuf entre versiones
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import grpc
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.assistant.embedded.v1alpha2 import (
    embedded_assistant_pb2,
    embedded_assistant_pb2_grpc
)

SCOPES = ['https://www.googleapis.com/auth/assistant-sdk-prototype']
ASSISTANT_ENDPOINT = 'embeddedassistant.googleapis.com'

def obtener_credenciales():
    """Carga o solicita las credenciales OAuth2."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as f:
            f.write(creds.to_json())
            
    return creds

def enviar_orden(comando_texto: str) -> str:
    """Envía un comando de texto al Asistente y devuelve su respuesta textual."""
    creds = obtener_credenciales()

    channel = grpc.secure_channel(
        ASSISTANT_ENDPOINT,
        grpc.composite_channel_credentials(
            grpc.ssl_channel_credentials(),
            grpc.access_token_call_credentials(creds.token)
        )
    )
    assistant = embedded_assistant_pb2_grpc.EmbeddedAssistantStub(channel)

    config = embedded_assistant_pb2.AssistConfig(
        text_query=comando_texto,
        audio_out_config=embedded_assistant_pb2.AudioOutConfig(
            encoding='LINEAR16', sample_rate_hertz=16000, volume_percentage=0
        ),
        device_config=embedded_assistant_pb2.DeviceConfig(
            device_id='script_local',
            device_model_id='script_model'
        )
    )

    peticion = embedded_assistant_pb2.AssistRequest(config=config)

    respuesta_asistente = ""
    for respuesta in assistant.Assist(iter([peticion])):
        if respuesta.dialog_state_out.supplemental_display_text:
            respuesta_asistente += respuesta.dialog_state_out.supplemental_display_text

    return respuesta_asistente.strip()

def encender_luz_si_esta_apagada(nombre_dispositivo: str = "luz del salón"):
    """Comprueba el estado del dispositivo antes de enviar la orden de encendido."""
    print(f"🔍 Comprobando estado de '{nombre_dispositivo}'...")
    
    # 1. Consultar estado
    pregunta = f"¿Está encendida la {nombre_dispositivo}?"
    respuesta_estado = enviar_orden(pregunta)
    print(f"💬 Respuesta de Google Home: '{respuesta_estado}'")

    respuesta_lower = respuesta_estado.lower()

    # 2. Evaluar la respuesta
    # Si la respuesta contiene "encendida" y no dice "apagada", ya está encendida
    if "encendid" in respuesta_lower and "apagad" not in respuesta_lower:
        print(f"💡 La {nombre_dispositivo} ya está encendida. No se realiza ninguna acción.")
    else:
        print(f"🔌 La {nombre_dispositivo} está apagada (o indeterminada). Enviando orden de encendido...")
        orden = f"Enciende la {nombre_dispositivo}"
        confirmacion = enviar_orden(orden)
        print(f"✅ Resultado: {confirmacion}")

if __name__ == "__main__":
    encender_luz_si_esta_apagada("luz del salón")