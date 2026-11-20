from typing import Literal
from pydantic import BaseModel, Field

class LoanApplication(BaseModel):
    amount: float = Field(..., gt=0, description="requested loan amount")
    term_months: int = Field(..., ge=6, le=60, description="loan term in months(6-60)")
    is_employed: bool
    monthly_income: float = Field(..., ge=0, description="net montly inc")
    collateral_value: float = Field(default=0.0, ge=0, description="value of assets")
    
class DecisionResponse(BaseModel):
    decision: Literal["approve", "decline", "refer"]
    interest_rate: float
    ai_score: float
    reason_trail: list[str]