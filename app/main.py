from fastapi import FastAPI

from app.decision import evaluate_application
from app.decision import DecisionResponse, LoanApplication

app = FastAPI(
    title="Decision api",
    description="evaluate loan application using business rules and a AI risk score",
    version="1.0.0",
)

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/decision", response_model=DecisionResponse)
def make_decision(application: LoanApplication) -> DecisionResponse:
    return evaluate_application(application)