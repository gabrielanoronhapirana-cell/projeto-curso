"""
RetailBot AI — FastAPI REST API
Provides HTTP endpoints for chat, session management, and health checks.
"""

import logging
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.agent import get_agent
from app.config import get_settings
from app.models import ChatRequest, ChatResponse, LGPDConsent

logger = logging.getLogger("retailbot.api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: initialize agent on startup."""
    settings = get_settings()
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    )
    logger.info("🤖 RetailBot AI starting up...")
    logger.info(f"   Environment: {settings.app_env}")
    logger.info(f"   Model: {settings.gemini_model}")
    
    # Pre-initialize the agent
    get_agent()
    logger.info("✅ Agent initialized successfully.")
    
    yield
    
    logger.info("👋 RetailBot AI shutting down.")


app = FastAPI(
    title="RetailBot AI",
    description="Intelligent omnichannel conversational agent for retail and e-commerce.",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ────────────────────────────────────────────────────────
# Endpoints
# ────────────────────────────────────────────────────────

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "RetailBot AI",
        "version": "0.1.0",
    }


@app.post("/session/create")
async def create_session():
    """Create a new chat session and return the session ID."""
    session_id = str(uuid.uuid4())
    agent = get_agent()
    agent.get_or_create_session(session_id)
    return {"session_id": session_id}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message and receive the agent's response.
    
    The agent handles:
    - LGPD consent verification
    - Product stock queries
    - Click & Collect reservations
    - Order tracking
    - FAQ/institutional questions
    - Human handoff when needed
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="A mensagem não pode estar vazia.")

    agent = get_agent()
    
    logger.info(f"[{request.session_id}] User: {request.message[:100]}...")
    
    reply = await agent.chat(request.session_id, request.message)
    
    logger.info(f"[{request.session_id}] Bot: {reply[:100]}...")

    session = agent.get_or_create_session(request.session_id)

    return ChatResponse(
        session_id=request.session_id,
        reply=reply,
        metadata={
            "lgpd_consent": session.lgpd_consent.value,
            "turn_count": len(session.conversation_history) // 2,
        },
    )


@app.post("/session/{session_id}/lgpd-consent")
async def update_lgpd_consent(session_id: str, accepted: bool = True):
    """Update LGPD consent status for a session."""
    agent = get_agent()
    session = agent.get_or_create_session(session_id)
    session.lgpd_consent = LGPDConsent.ACCEPTED if accepted else LGPDConsent.REJECTED
    return {
        "session_id": session_id,
        "lgpd_consent": session.lgpd_consent.value,
    }


@app.get("/session/{session_id}/history")
async def get_session_history(session_id: str):
    """Retrieve conversation history for a session."""
    agent = get_agent()
    if session_id not in agent.sessions:
        raise HTTPException(status_code=404, detail="Sessão não encontrada.")
    
    session = agent.sessions[session_id]
    return {
        "session_id": session_id,
        "history": session.conversation_history,
        "turn_count": len(session.conversation_history) // 2,
    }


@app.get("/stores")
async def list_stores():
    """List all available store locations."""
    from app.tools import get_available_stores
    stores = get_available_stores()
    return {
        "stores": [
            {"store_id": sid, "name": name}
            for sid, name in stores.items()
        ]
    }


@app.get("/products")
async def list_products():
    """List all products in the catalog."""
    from app.tools import get_product_catalog
    catalog = get_product_catalog()
    return {
        "products": [
            {"sku": sku, **details}
            for sku, details in catalog.items()
        ]
    }
