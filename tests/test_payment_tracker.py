from payment_tracker import Payment, PaymentTracker
import pytest
from datetime import datetime, timedelta

def test_get_payment_status():
    tracker = PaymentTracker()
    payment = Payment(1, "pending", datetime.now())
    tracker.add_payment(payment)
    assert tracker.get_payment_status(1) == "pending"

def test_get_payment_status_not_found():
    tracker = PaymentTracker()
    assert tracker.get_payment_status(1) == "not_found"

def test_update_payment_status():
    tracker = PaymentTracker()
    payment = Payment(1, "pending", datetime.now())
    tracker.add_payment(payment)
    tracker.update_payment_status(1, "cleared")
    assert tracker.get_payment_status(1) == "cleared"

def test_get_payment():
    tracker = PaymentTracker()
    payment = Payment(1, "pending", datetime.now())
    tracker.add_payment(payment)
    result = tracker.get_payment(1)
    assert result["id"] == 1
    assert result["status"] == "pending"
    assert result["estimated_arrival_time"] == payment.estimated_arrival_time.isoformat()

def test_get_payment_not_found():
    tracker = PaymentTracker()
    result = tracker.get_payment(1)
    assert result == {"error": "not_found"}
