"""Pydantic domain models for the RetailBot AI application."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class LGPDConsent(str, Enum):
    """LGPD (Lei Geral de Proteção de Dados) consent status."""

    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class CustomerSession(BaseModel):
    """Represents an active customer chat session."""

    session_id: str
    customer_id: Optional[str] = None
    customer_name: Optional[str] = None
    lgpd_consent: LGPDConsent = LGPDConsent.PENDING
    conversation_history: list[dict] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)


class ChatRequest(BaseModel):
    """Incoming chat message from a customer."""

    session_id: str
    message: str


class ChatResponse(BaseModel):
    """Outgoing chat reply to a customer."""

    session_id: str
    reply: str
    metadata: Optional[dict] = None


class StockResult(BaseModel):
    """Result of a stock availability check for a given SKU and store."""

    sku: str
    store_id: str
    store_name: str
    quantity: int
    price: float
    available: bool


class ReservationResult(BaseModel):
    """Result of a product reservation request."""

    reservation_code: str
    sku: str
    store_id: str
    customer_id: str
    expires_at: datetime
    status: str = "active"


class OrderStatus(BaseModel):
    """Current status of a customer order."""

    order_id: str
    status: str
    tracking_code: Optional[str] = None
    estimated_delivery: Optional[str] = None
    items: list[dict] = Field(default_factory=list)
    last_update: Optional[datetime] = None


class HandoffRequest(BaseModel):
    """Request to hand off a conversation to a human agent."""

    reason: str
    problem: str
    context: str
    recommended_action: str


class HandoffResult(BaseModel):
    """Result after a handoff request has been processed."""

    ticket_id: str
    status: str
    message: str
    priority_followup: bool = False
