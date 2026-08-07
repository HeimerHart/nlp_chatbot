import random

_MERCHANTS = ["Burger King", "Domino's Pizza", "Subway", "KFC", "Chai Point"]
_ORDER_STATUSES = [
    ("Order Placed", 5),
    ("Preparing", 15),
    ("Out for Delivery", 25),
    ("Preparing", 12),
]

REFUND_STAGES = ["Refund Requested", "Approved", "Processing", "Refunded"]


def simulated_order_status(order_id: str | None = None) -> dict:
    merchant = random.choice(_MERCHANTS)
    status, eta_minutes = random.choice(_ORDER_STATUSES)
    return {
        "type": "order_status",
        "order_id": order_id or f"DEMO-{random.randint(10000, 99999)}",
        "merchant": merchant,
        "status": status,
        "eta_minutes": eta_minutes,
        "demo": True,
    }


def simulated_refund_timeline(order_id: str | None = None) -> dict:
    current_index = random.choice([0, 1, 2])
    return {
        "type": "refund_timeline",
        "order_id": order_id or f"DEMO-{random.randint(10000, 99999)}",
        "stages": REFUND_STAGES,
        "current_stage_index": current_index,
        "expected_window": "3-5 business days",
        "demo": True,
    }
