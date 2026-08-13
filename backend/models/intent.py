from enum import Enum


class Intent(str, Enum):
    GREETING = "greeting"
    ORDER_TRACKING = "order_tracking"
    REFUND = "refund"
    PAYMENT_ISSUE = "payment_issue"
    ORDER_ISSUE = "order_issue"
    DELIVERY_PARTNER = "delivery_partner"
    ACCOUNT_SUPPORT = "account_support"
    HUMAN_AGENT = "human_agent"
    SMALLTALK = "smalltalk"
    UNKNOWN = "unknown"


INTENT_LABELS = {
    Intent.ORDER_TRACKING: "Order tracking",
    Intent.REFUND: "Refunds",
    Intent.PAYMENT_ISSUE: "Payment issues",
    Intent.ORDER_ISSUE: "Wrong or missing item",
    Intent.DELIVERY_PARTNER: "Delivery partner",
    Intent.ACCOUNT_SUPPORT: "Account support",
    Intent.HUMAN_AGENT: "Talk to a human",
    Intent.SMALLTALK: "Just chatting",
}

DATASET_LABEL_TO_INTENT = {
    "greeting": Intent.GREETING,
    "refund": Intent.REFUND,
    "login": Intent.ACCOUNT_SUPPORT,
    "order_status": Intent.ORDER_TRACKING,
    "payment": Intent.PAYMENT_ISSUE,
    "agent": Intent.HUMAN_AGENT,
    "smalltalk": Intent.SMALLTALK,
}
