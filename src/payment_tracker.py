import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict

@dataclass
class Payment:
    id: int
    status: str
    estimated_arrival_time: datetime

class PaymentTracker:
    def __init__(self):
        self.payments: Dict[int, Payment] = {}

    def add_payment(self, payment: Payment):
        self.payments[payment.id] = payment

    def get_payment_status(self, payment_id: int) -> str:
        payment = self.payments.get(payment_id)
        if payment:
            return payment.status
        return "not_found"

    def update_payment_status(self, payment_id: int, new_status: str):
        payment = self.payments.get(payment_id)
        if payment:
            payment.status = new_status
            if new_status == "cleared":
                payment.estimated_arrival_time = datetime.now() + timedelta(seconds=30)

    def get_payment(self, payment_id: int) -> Dict:
        payment = self.payments.get(payment_id)
        if payment:
            return {
                "id": payment.id,
                "status": payment.status,
                "estimated_arrival_time": payment.estimated_arrival_time.isoformat()
            }
        return {"error": "not_found"}
