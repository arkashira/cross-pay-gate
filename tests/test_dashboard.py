import pytest
from dashboard import Dashboard, Payment
from datetime import datetime

def test_add_payment():
    dashboard = Dashboard()
    payment = Payment('123', 100.0, 'Destination', 'Pending', 1.0, '2024-09-16')
    dashboard.add_payment(payment)
    assert len(dashboard.payments) == 1

def test_get_payments():
    dashboard = Dashboard()
    payment1 = Payment('123', 100.0, 'Destination', 'Pending', 1.0, '2024-09-16')
    payment2 = Payment('456', 200.0, 'Destination', 'Processed', 2.0, '2024-09-17')
    dashboard.add_payment(payment1)
    dashboard.add_payment(payment2)
    payments = dashboard.get_payments()
    assert len(payments) == 2

def test_get_payments_date_range():
    dashboard = Dashboard()
    payment1 = Payment('123', 100.0, 'Destination', 'Pending', 1.0, '2024-09-16')
    payment2 = Payment('456', 200.0, 'Destination', 'Processed', 2.0, '2024-09-17')
    dashboard.add_payment(payment1)
    dashboard.add_payment(payment2)
    start_date = datetime(2024, 9, 15)
    end_date = datetime(2024, 9, 16)
    payments = dashboard.get_payments((start_date, end_date))
    assert len(payments) == 1

def test_get_payments_status():
    dashboard = Dashboard()
    payment1 = Payment('123', 100.0, 'Destination', 'Pending', 1.0, '2024-09-16')
    payment2 = Payment('456', 200.0, 'Destination', 'Processed', 2.0, '2024-09-17')
    dashboard.add_payment(payment1)
    dashboard.add_payment(payment2)
    payments = dashboard.get_payments(status='Pending')
    assert len(payments) == 1

def test_export_to_csv():
    dashboard = Dashboard()
    payment1 = Payment('123', 100.0, 'Destination', 'Pending', 1.0, '2024-09-16')
    dashboard.add_payment(payment1)
    csv_data = dashboard.export_to_csv(dashboard.payments)
    assert csv_data == 'payment_id,amount,destination,status,fee,eta\n123,100.0,Destination,Pending,1.0,2024-09-16\n'

def test_update_status():
    dashboard = Dashboard()
    payment1 = Payment('123', 100.0, 'Destination', 'Pending', 1.0, '2024-09-16')
    dashboard.add_payment(payment1)
    dashboard.update_status('123', 'Processed')
    assert dashboard.payments[0].status == 'Processed'
