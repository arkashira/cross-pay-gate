import json
from dataclasses import dataclass
from typing import Dict

@dataclass
class Transaction:
    amount: float
    currency: str
    source: str
    destination: str
    reference: str

class APIGateway:
    def __init__(self):
        self.correspondent_banks = {
            "USD": {"bank1": 0.01, "bank2": 0.02},
            "EUR": {"bank3": 0.03, "bank4": 0.04}
        }
        self.transactions = {}

    def initiate_payment(self, payload: Dict) -> Dict:
        try:
            transaction = Transaction(**payload)
        except TypeError:
            raise TypeError("Invalid payload type")
        if not isinstance(transaction.amount, (int, float)) or transaction.amount <= 0:
            raise TypeError("Invalid amount type or value")
        transaction_id = len(self.transactions) + 1
        self.transactions[transaction_id] = transaction
        optimal_bank = self.get_optimal_bank(transaction.currency)
        return {"transaction_id": transaction_id, "status_endpoint": f"/status/{transaction_id}"}

    def get_optimal_bank(self, currency: str) -> str:
        banks = self.correspondent_banks.get(currency, {})
        return min(banks, key=banks.get)

    def get_status(self, transaction_id: int) -> Dict:
        transaction = self.transactions.get(transaction_id)
        if transaction:
            return {"status": "processing", "transaction_id": transaction_id}
        return {"status": "not_found", "transaction_id": transaction_id}
