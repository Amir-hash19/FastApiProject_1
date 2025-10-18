from decimal import Decimal
from core.tests.conftest import auth_client

def test_create_payment(auth_client, db_session, auth_user):
    """the test check out the endpoint for creating payment"""

    db_session.add(auth_user)
    db_session.commit()
    db_session.refresh(auth_user)

    payload = {"amount": "5000.00", "description": "Test payment"}
    response = auth_client.post("/api/v1/payment", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["message"] == "Payment created successfully"
    assert "id" in data
    assert data["id"] > 0
    assert Decimal(data["amount"]) == Decimal("5000.00")
    assert data["description"] == "Test payment"



from fastapi import status
def test_get_payment_not_found(auth_client, db_session, auth_user):
    """here we check that if not payment exist status code and message raise successfully"""
 
    db_session.add(auth_user)
    db_session.commit()
    db_session.refresh(auth_user)

    
    response = auth_client.get("/api/v1/payments/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data.get("status") == "Payment Not Found"
    assert "message" in data


def test_delete_payment_not_found(auth_client, db_session, auth_user):
    """delete not exist payment and check status code and meaages"""
    db_session.add(auth_user)
    db_session.commit()
    db_session.refresh(auth_user)


    response = auth_client.delete("/api/v1/payments/999")  
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert data.get("status") == "Payment Not Found"
    assert response.status_code == 404
    assert "message" in data



