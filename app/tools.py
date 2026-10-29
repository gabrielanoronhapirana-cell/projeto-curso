"""
RetailBot AI — Mock Tool Functions
Simulate ERP, inventory, and CRM backend calls.
"""

import random
import string
import asyncio
from datetime import datetime, timedelta
from app.models import StockResult, ReservationResult, OrderStatus, HandoffResult

# --- Mock Data ---
MOCK_STORES = {
    "SP001": "Loja Centro - São Paulo",
    "SP002": "Loja Pinheiros - São Paulo",
    "RJ001": "Loja Copacabana - Rio de Janeiro",
    "BH001": "Loja Savassi - Belo Horizonte",
    "CWB001": "Loja Batel - Curitiba",
}

MOCK_PRODUCTS = {
    "SKU-1001": {"name": "Tênis Runner Pro", "price": 349.90, "category": "Calçados"},
    "SKU-1002": {"name": "Camiseta Básica Algodão", "price": 79.90, "category": "Vestuário"},
    "SKU-1003": {"name": "Mochila Urban 30L", "price": 199.90, "category": "Acessórios"},
    "SKU-2001": {"name": "Jaqueta Corta-Vento", "price": 259.90, "category": "Vestuário"},
    "SKU-2002": {"name": "Boné Lifestyle", "price": 89.90, "category": "Acessórios"},
    "SKU-3001": {"name": "Short Esportivo Dry-Fit", "price": 119.90, "category": "Vestuário"},
}

MOCK_ORDERS = {
    "ORD-50001": {
        "status": "em_transito",
        "tracking_code": "BR123456789YZ",
        "estimated_delivery": "02/11/2026",
        "items": [{"sku": "SKU-1001", "name": "Tênis Runner Pro", "qty": 1}],
        "last_update": datetime(2026, 10, 28, 14, 30),
    },
    "ORD-50002": {
        "status": "entregue",
        "tracking_code": "BR987654321YZ",
        "estimated_delivery": "27/10/2026",
        "items": [
            {"sku": "SKU-1002", "name": "Camiseta Básica Algodão", "qty": 2},
            {"sku": "SKU-2002", "name": "Boné Lifestyle", "qty": 1},
        ],
        "last_update": datetime(2026, 10, 27, 10, 15),
    },
    "ORD-50003": {
        "status": "processando",
        "tracking_code": None,
        "estimated_delivery": "05/11/2026",
        "items": [{"sku": "SKU-1003", "name": "Mochila Urban 30L", "qty": 1}],
        "last_update": datetime(2026, 10, 29, 9, 0),
    },
}


def _generate_reservation_code() -> str:
    """Generate a 24-hour alphanumeric reservation code."""
    return "RES-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))


async def check_stock(sku: str, store_id: str) -> StockResult:
    """
    Check real-time stock for a given SKU at a specific store.
    Simulates ERP call with <400ms latency.
    """
    await asyncio.sleep(random.uniform(0.05, 0.2))  # Simulate ERP latency

    product = MOCK_PRODUCTS.get(sku)
    store_name = MOCK_STORES.get(store_id)

    if not product:
        return StockResult(
            sku=sku, store_id=store_id, store_name=store_name or "Desconhecida",
            quantity=0, price=0.0, available=False,
        )

    if not store_name:
        return StockResult(
            sku=sku, store_id=store_id, store_name="Loja não encontrada",
            quantity=0, price=0.0, available=False,
        )

    # Simulate random stock levels
    quantity = random.randint(0, 15)
    return StockResult(
        sku=sku, store_id=store_id, store_name=store_name,
        quantity=quantity, price=product["price"], available=quantity > 0,
    )


async def create_reservation(sku: str, store_id: str, customer_id: str) -> ReservationResult:
    """
    Create an express Click & Collect reservation.
    Reservation is valid for 24 hours.
    """
    await asyncio.sleep(random.uniform(0.1, 0.3))  # Simulate processing

    product = MOCK_PRODUCTS.get(sku)
    store_name = MOCK_STORES.get(store_id)

    if not product or not store_name:
        raise ValueError(f"Produto (SKU: {sku}) ou loja ({store_id}) não encontrado(a).")

    code = _generate_reservation_code()
    return ReservationResult(
        reservation_code=code,
        sku=sku,
        store_id=store_id,
        customer_id=customer_id,
        expires_at=datetime.now() + timedelta(hours=24),
        status="active",
    )


async def get_order_status(order_id: str) -> OrderStatus | None:
    """
    Retrieve shipping timeline and delivery status for an order.
    """
    await asyncio.sleep(random.uniform(0.05, 0.15))

    order = MOCK_ORDERS.get(order_id.upper())
    if not order:
        return None

    return OrderStatus(
        order_id=order_id.upper(),
        status=order["status"],
        tracking_code=order.get("tracking_code"),
        estimated_delivery=order.get("estimated_delivery"),
        items=order.get("items", []),
        last_update=order.get("last_update"),
    )


async def trigger_handoff(reason: str, problem: str, context: str, recommended_action: str) -> HandoffResult:
    """
    Trigger human handoff (transbordo) and generate a support ticket.
    """
    await asyncio.sleep(0.1)

    ticket_id = "TKT-" + "".join(random.choices(string.digits, k=6))

    # Check if within business hours (Mon-Sat, 08:00-20:00 BRT)
    now = datetime.now()
    is_business_hours = (
        now.weekday() < 6  # Mon=0 to Sat=5
        and 8 <= now.hour < 20
    )

    if is_business_hours:
        return HandoffResult(
            ticket_id=ticket_id,
            status="transferido",
            message=f"Chamado {ticket_id} criado. Transferindo para um atendente humano agora.",
            priority_followup=False,
        )
    else:
        return HandoffResult(
            ticket_id=ticket_id,
            status="fora_do_horario",
            message=f"Chamado {ticket_id} criado. Nosso horário de atendimento é de segunda a sábado, das 08h às 20h. Você receberá atendimento prioritário no próximo dia útil.",
            priority_followup=True,
        )


def get_available_stores() -> dict[str, str]:
    """Return all available stores."""
    return MOCK_STORES.copy()


def get_product_catalog() -> dict[str, dict]:
    """Return the product catalog."""
    return MOCK_PRODUCTS.copy()
