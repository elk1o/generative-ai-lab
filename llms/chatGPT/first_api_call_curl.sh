export OPENAI_API_KEY=$(python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('OPENAI_APIKEY'))")

curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [
      {"role": "user", "content": "¿Puedes decirme que agente de IA eres? Es mi primera llamada remota de API de la IA"}
    ]
  }'