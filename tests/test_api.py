"""
RetailBot AI — Test Suite
Tests for tools, knowledge base, models, and API endpoints.
Run with: pytest tests/ -v
"""

import pytest
import asyncio
from datetime import datetime, timedelta

from app.models import (
    CustomerSession, ChatRequest, ChatResponse, StockResult,
    ReservationResult, OrderStatus, HandoffResult, LGPDConsent,
)
from app.tools import (
    check_stock, create_reservation, get_order_status,
    trigger_handoff, get_available_stores, get_product_catalog,
)
from app.knowledge_base import search_knowledge_base


# ────────────────────────────────────────────────────────
# Model Tests
# ────────────────────────────────────────────────────────

class TestModels:
    def test_customer_session_defaults(self):
        session = CustomerSession(session_id="test-123")
        assert session.session_id == "test-123"
        assert session.customer_id is None
        assert session.lgpd_consent == LGPDConsent.PENDING
        assert session.conversation_history == []

    def test_chat_request_validation(self):
        req = ChatRequest(session_id="s1", message="Olá!")
        assert req.session_id == "s1"
        assert req.message == "Olá!"

    def test_stock_result(self):
        result = StockResult(
            sku="SKU-1001", store_id="SP001", store_name="Test",
            quantity=5, price=349.90, available=True,
        )
        assert result.available is True
        assert result.quantity == 5

    def test_lgpd_consent_enum(self):
        assert LGPDConsent.PENDING.value == "pending"
        assert LGPDConsent.ACCEPTED.value == "accepted"
        assert LGPDConsent.REJECTED.value == "rejected"


# ────────────────────────────────────────────────────────
# Tool Tests
# ────────────────────────────────────────────────────────

class TestTools:
    @pytest.mark.asyncio
    async def test_check_stock_valid(self):
        result = await check_stock("SKU-1001", "SP001")
        assert result.sku == "SKU-1001"
        assert result.store_id == "SP001"
        assert result.store_name == "Loja Centro - São Paulo"
        assert result.price == 349.90
        assert isinstance(result.quantity, int)

    @pytest.mark.asyncio
    async def test_check_stock_invalid_sku(self):
        result = await check_stock("INVALID-SKU", "SP001")
        assert result.available is False
        assert result.quantity == 0

    @pytest.mark.asyncio
    async def test_check_stock_invalid_store(self):
        result = await check_stock("SKU-1001", "INVALID")
        assert result.available is False
        assert result.store_name == "Loja não encontrada"

    @pytest.mark.asyncio
    async def test_create_reservation_valid(self):
        result = await create_reservation("SKU-1001", "SP001", "CUST-001")
        assert result.reservation_code.startswith("RES-")
        assert len(result.reservation_code) == 12  # RES- + 8 chars
        assert result.sku == "SKU-1001"
        assert result.store_id == "SP001"
        assert result.customer_id == "CUST-001"
        assert result.status == "active"
        assert result.expires_at > datetime.now()

    @pytest.mark.asyncio
    async def test_create_reservation_invalid_sku(self):
        with pytest.raises(ValueError):
            await create_reservation("INVALID", "SP001", "CUST-001")

    @pytest.mark.asyncio
    async def test_get_order_status_valid(self):
        result = await get_order_status("ORD-50001")
        assert result is not None
        assert result.order_id == "ORD-50001"
        assert result.status == "em_transito"
        assert result.tracking_code == "BR123456789YZ"

    @pytest.mark.asyncio
    async def test_get_order_status_not_found(self):
        result = await get_order_status("ORD-99999")
        assert result is None

    @pytest.mark.asyncio
    async def test_trigger_handoff(self):
        result = await trigger_handoff(
            reason="customer_request",
            problem="Cliente quer trocar produto",
            context="SKU-1001, Loja SP001",
            recommended_action="Processar troca",
        )
        assert result.ticket_id.startswith("TKT-")
        assert result.status in ("transferido", "fora_do_horario")

    def test_get_available_stores(self):
        stores = get_available_stores()
        assert len(stores) == 5
        assert "SP001" in stores
        assert "RJ001" in stores

    def test_get_product_catalog(self):
        catalog = get_product_catalog()
        assert len(catalog) == 6
        assert "SKU-1001" in catalog
        assert catalog["SKU-1001"]["name"] == "Tênis Runner Pro"


# ────────────────────────────────────────────────────────
# Knowledge Base Tests
# ────────────────────────────────────────────────────────

class TestKnowledgeBase:
    def test_search_returns_policy(self):
        result = search_knowledge_base("Qual a política de troca e devolução?")
        assert result is not None
        assert "30 dias" in result

    def test_search_payment_methods(self):
        result = search_knowledge_base("Quais formas de pagamento vocês aceitam?")
        assert result is not None
        assert "Pix" in result

    def test_search_store_hours(self):
        result = search_knowledge_base("Qual o horário de funcionamento?")
        assert result is not None
        assert "Segunda" in result

    def test_search_shipping(self):
        result = search_knowledge_base("Como funciona o frete?")
        assert result is not None
        assert "Frete grátis" in result

    def test_search_click_collect(self):
        result = search_knowledge_base("Como faço para reservar e retirar na loja?")
        assert result is not None
        assert "24 horas" in result

    def test_search_lgpd(self):
        result = search_knowledge_base("Como vocês tratam meus dados? LGPD")
        assert result is not None
        assert "LGPD" in result

    def test_search_no_match(self):
        result = search_knowledge_base("xyzzy foobar gibberish")
        assert result is None

    def test_search_loyalty_program(self):
        result = search_knowledge_base("programa de fidelidade pontos")
        assert result is not None
        assert "RetailClub" in result


# ────────────────────────────────────────────────────────
# API Endpoint Tests (no LLM required)
# ────────────────────────────────────────────────────────

class TestAPI:
    """Tests for non-LLM API endpoints."""

    @pytest.fixture
    def client(self):
        """Create a test client. Requires GEMINI_API_KEY in env (can be dummy for non-chat tests)."""
        import os
        os.environ.setdefault("GEMINI_API_KEY", "test-key-for-non-chat-tests")
        
        from fastapi.testclient import TestClient
        from app.api import app
        
        with TestClient(app) as c:
            yield c

    def test_health(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "RetailBot AI"

    def test_create_session(self, client):
        response = client.post("/session/create")
        assert response.status_code == 200
        data = response.json()
        assert "session_id" in data
        assert len(data["session_id"]) > 0

    def test_list_stores(self, client):
        response = client.get("/stores")
        assert response.status_code == 200
        data = response.json()
        assert "stores" in data
        assert len(data["stores"]) == 5

    def test_list_products(self, client):
        response = client.get("/products")
        assert response.status_code == 200
        data = response.json()
        assert "products" in data
        assert len(data["products"]) == 6

    def test_session_not_found(self, client):
        response = client.get("/session/nonexistent-id/history")
        assert response.status_code == 404

    def test_empty_message_rejected(self, client):
        # Create a session first
        session_resp = client.post("/session/create")
        session_id = session_resp.json()["session_id"]
        
        response = client.post("/chat", json={
            "session_id": session_id,
            "message": "   ",
        })
        assert response.status_code == 400


# ────────────────────────────────────────────────────────
# CPF Masking Tests
# ────────────────────────────────────────────────────────

class TestCPFMasking:
    def test_mask_cpf(self):
        from app.agent import mask_cpf
        assert mask_cpf("123.456.789-00") == "***.456.789-**"
        assert mask_cpf("12345678900") == "***.456.789-**"

    def test_mask_cpf_invalid(self):
        from app.agent import mask_cpf
        # Should return as-is for invalid CPFs
        assert mask_cpf("123") == "123"
