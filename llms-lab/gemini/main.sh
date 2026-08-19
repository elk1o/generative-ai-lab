export AISTUDIO_APIKEY=$(python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('AISTUDIO_APIKEY'))")

curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent" \
  -H 'Content-Type: application/json' \
  -H "X-goog-api-key: $AISTUDIO_APIKEY" \
  -X POST \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "¿Puedes decirme que agente de IA eres? Es mi primera llamada remota de API de la IA"
          }
        ]
      }
    ]
  }'