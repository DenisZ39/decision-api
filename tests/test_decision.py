from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    
def test_decision_approve() -> None:
    payload = {
        "amount": 10000,
        "term_months": 24,
        "is_employed": True,
        "monthly_income": 3000,
        "collateral_value": 0,
    }
    response = client.post("/decision", json = payload)
    data = response.json()
    
    assert response.status_code == 200
    assert data["decision"] == "approve"
    assert data["interest_rate"] == 5.5
    assert data["ai_score"] >= 0.70
    assert len(data["reason_trail"]) == 4
    
def test_decision_decline_unaffordable() -> None:
    payload = {
        "amount": 20000,
        "term_months": 12,
        "is_employed": True,
        "monthly_income": 2000,
        "collateral_value": 0,
    }
    response = client.post ("/decision", json=payload)
    data = response.json()
    
    assert response.status_code == 200
    assert data["decision"] == "decline"
    assert data["interest_rate"] == 0.0
    assert any("affordability" in reason.lower() and "failed" in reason.lower() for reason in data["reason_trail"])
    
def test_decision_refer_high_amount_low_collateral() -> None:
    payload = {
        "amount": 60000,
        "term_months": 60,
        "is_employed": True,
        "monthly_income": 5000,
        "collateral_value": 10000,
    }
    response = client.post("/decision", json=payload)
    data = response.json()
    
    assert response.status_code == 200
    assert data["decision"] == "refer"
    assert data["interest_rate"] == 9.5
    assert any("collateral" in reason.lower() and "flagged" in reason.lower() for reason in data["reason_trail"])
    
def test_invalid_payload_returns_422() -> None:
    payload = {
        "amount": -500,
        "term_months": 3,
        "is_employed": True,
        "monthly_income": 3000,
    }
    response = client.post("/decision", json=payload)
    assert response.status_code == 422