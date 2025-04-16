import frappe

@frappe.whitelist()
def get_order_stats():
    orders = [
        {"order_id": "ORD001", "status": "Open", "order_price": "150"},
        {"order_id": "ORD002", "status": "Closed", "order_price": "245"},
        {"order_id": "ORD003", "status": "Open", "order_price": "100"}
    ]

    return {
        "total_orders": 1250,
        "pending_orders": 310,
        "delivered": 900,
        "cancelled": 50,
        "orders": orders
    }
