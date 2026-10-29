# 🤖 RetailBot AI

An intelligent omnichannel conversational agent for retail and e-commerce, powered by **Google Gemini**.

## Features

- 🛍️ **Real-time Stock Checks** — Query product availability across store locations
- 🛒 **Click & Collect Reservations** — Express 24-hour product reservations
- 📦 **Order Tracking** — Real-time order status and shipping updates
- 📋 **Institutional FAQ** — Automated answers for policies, returns, payments, and more
- 🔒 **LGPD Compliance** — Built-in consent management and data masking
- 🔄 **Smart Handoff** — Automatic escalation to human agents when needed
- 🇧🇷 **Brazilian Portuguese** — Native pt-BR conversational experience

## Tech Stack

- **Runtime:** Python 3.11+
- **Framework:** FastAPI + Uvicorn
- **AI Engine:** Google Gemini (via `google-genai` SDK)
- **Data Validation:** Pydantic v2

## Quick Start

### 1. Prerequisites
- Python 3.11 or higher
- A [Google AI Studio](https://aistudio.google.com/) API key

### 2. Installation

```bash
# Clone and enter the project
cd retailbot-ai

# Create a virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -e .
```

### 3. Configuration

```bash
# Copy the environment template
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your-api-key-here
```

### 4. Run the Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/session/create` | Create a new chat session |
| `POST` | `/chat` | Send a message and get a response |
| `POST` | `/session/{id}/lgpd-consent` | Update LGPD consent |
| `GET` | `/session/{id}/history` | Get conversation history |
| `GET` | `/stores` | List available stores |
| `GET` | `/products` | List product catalog |

### Example: Chat

```bash
# Create a session
curl -X POST http://localhost:8000/session/create

# Send a message
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "YOUR_SESSION_ID",
    "message": "Olá! Quero verificar se o Tênis Runner Pro está disponível na loja de Pinheiros."
  }'
```

## Architecture

```
retailbot-ai/
├── app/
│   ├── __init__.py          # Package init
│   ├── agent.py             # Core Gemini-powered agent engine
│   ├── api.py               # FastAPI REST endpoints
│   ├── config.py            # Settings & configuration
│   ├── knowledge_base.py    # FAQ knowledge base (simulated RAG)
│   ├── models.py            # Pydantic data models
│   └── tools.py             # Mock tool functions (ERP simulation)
├── main.py                  # Application entry point
├── pyproject.toml           # Project configuration
├── .env.example             # Environment template
└── README.md                # This file
```

## Mock Data

The project includes mock data for testing:

**Stores:** SP001, SP002, RJ001, BH001, CWB001  
**Products:** SKU-1001 through SKU-3001 (shoes, clothing, accessories)  
**Orders:** ORD-50001, ORD-50002, ORD-50003

## License

MIT
