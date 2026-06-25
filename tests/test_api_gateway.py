import pytest
from src.api_gateway import APIGateway, Transaction

def test_initiate_payment():
    gateway = APIGateway()
    payload = {
        "amount": 100.0,
        "currency": "USD",
        "source": "source1",
        "destination": "destination1",
        "reference": "reference1"
    }
    response = gateway.initiate_payment(payload)
    assert response["transaction_id"] == 1
    assert response["status_endpoint"] == "/status/1"

def test_get_optimal_bank():
    gateway = APIGateway()
    optimal_bank = gateway.get_optimal_bank("USD")
    assert optimal_bank == "bank1"

def test_get_status():
    gateway = APIGateway()
    payload = {
        "amount": 100.0,
        "currency": "USD",
        "source": "source1",
        "destination": "destination1",
        "reference": "reference1"
    }
    response = gateway.initiate_payment(payload)
    transaction_id = response["transaction_id"]
    status = gateway.get_status(transaction_id)
    assert status["status"] == "processing"
    assert status["transaction_id"] == transaction_id

def test_get_status_not_found():
    gateway = APIGateway()
    status = gateway.get_status(1)
    assert status["status"] == "not_found"
    assert status["transaction_id"] == 1

def test_initiate_payment_invalid_payload():
    gateway = APIGateway()
    payload = {
        "amount": "invalid",
        "currency": "USD",
        "source": "source1",
        "destination": "destination1",
        "reference": "reference1"
    }
    with pytest.raises(TypeError):
        gateway.initiate_payment(payload)
