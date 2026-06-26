import json
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class Payment:
    payment_id: str
    amount: float
    destination: str
    status: str
    fee: float
    eta: str

class Dashboard:
    def __init__(self):
        self.payments = []

    def add_payment(self, payment: Payment):
        self.payments.append(payment)

    def get_payments(self, date_range: tuple = None, status: str = None, currency: str = None):
        filtered_payments = self.payments.copy()
        if date_range:
            start_date, end_date = date_range
            filtered_payments = [p for p in filtered_payments if start_date <= datetime.strptime(p.eta, '%Y-%m-%d') <= end_date]
        if status:
            filtered_payments = [p for p in filtered_payments if p.status == status]
        if currency:
            # Assuming currency is part of the amount (e.g., '100 USD')
            filtered_payments = [p for p in filtered_payments if currency in str(p.amount)]
        return filtered_payments

    def export_to_csv(self, payments: List[Payment]):
        csv_data = 'payment_id,amount,destination,status,fee,eta\n'
        for payment in payments:
            csv_data += f'{payment.payment_id},{payment.amount},{payment.destination},{payment.status},{payment.fee},{payment.eta}\n'
        return csv_data

    def update_status(self, payment_id: str, new_status: str):
        for payment in self.payments:
            if payment.payment_id == payment_id:
                payment.status = new_status
                break
