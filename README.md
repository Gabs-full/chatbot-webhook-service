# chatbot-webhook-service

Microserviço que **recebe mensagens do WhatsApp** via Evolution API, processa com IA e responde automaticamente.

---

## Como funciona

```
WhatsApp → Evolution API → POST /webhook/ → processa em background
                                                    ↓
                                         busca número no banco
                                                    ↓
                                         busca histórico
                                                    ↓
                                         chama OpenAI ou Claude
                                                    ↓
                                         salva resposta
                                                    ↓
                                         envia pelo WhatsApp
```

---

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| POST | `/webhook/` | Recebe eventos do WhatsApp |
| GET | `/health` | Health check |

---

## Setup local

```bash
pip install -r requirements.txt
cp .env.example .env
# edite o .env com suas chaves
uvicorn app.main:app --reload --port 8002
```

### Expor para internet (desenvolvimento)
```bash
ngrok http 8002
```

Configure o webhook na Evolution API com a URL do ngrok:
```
https://xxxx.ngrok.io/webhook/
```

---

## Variáveis de ambiente

| Variável | Descrição |
|---|---|
| `DATABASE_URL` | URL de conexão PostgreSQL |
| `OPENAI_KEY` | Chave da API OpenAI |
| `CLAUDE_KEY` | Chave da API Anthropic |
| `EVOLUTION_URL` | URL da Evolution API |
| `EVOLUTION_KEY` | API Key da Evolution API |
