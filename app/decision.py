from app.schemas import DecisionResponse, LoanApplication

def _calculate_ai_score(application: LoanApplication) -> float:
    """deterministic stub simulating an ML risk model (return 0.0 or 1.0)"""
    score = 0.50
    if application.is_employed:
        score += 0.20
    if application.collateral_value >= application.amount * 0.5:
        score += 0.15
    if application.monthly_income >= 0:
        estimated_payment = application.amount / application.term_months
        if estimated_payment <= application.monthly_income * 0.25:
            score += 0.10
        
    return round(min(score, 1.0), 20)

def evaluate_application(application: LoanApplication) -> DecisionResponse:
    reason_trail: list[str] = []
    hard_decline = False
    needs_review = False
    
    # Rule 1
    if application.is_employed:
        reason_trail.append("Rule 1 (employment): passed - applicant is currently employed")
    else:
        needs_review = True
        reason_trail.append("Rule 1 (employment): flagged - unemployed applicants require human review")
    
    # Rule 2
    estimated_monthly_payment = application.amount / application.term_months
    if application.monthly_income == 0 or estimated_monthly_payment > application.monthly_income * 0.40:
        hard_decline = True
        reason_trail.append(
            f"Rule 2 (Affordability): Failed - estimated payment ({estimated_monthly_payment:.2f})"
            f"exceeds 40% of monthly income ({application.monthly_income:.2f})"
        )
    else:
        reason_trail.append(
            f"Rule 2 (Affordability): Passed - estimated payment ({estimated_monthly_payment:.2f}) "
            "is within 40% of total income"
        )
    
    # Rule 3
    if application.amount > 50000 and application.collateral_value < application.amount * 0.5:
        needs_review = True
        reason_trail.append(
            "Rule 3 (Collateral): flagged - loans above 50,000 without 50% collateral require manual review"
        )
    else:
        reason_trail.append("Rule 3 (Collateral): passed - loan amount and collateral are within limits")
    
    ai_score = _calculate_ai_score(application)
    reason_trail.append(f"AI risk score: {ai_score:.2f} (auto approve threshold >= 0.70)")
    
    if ai_score < 0.50:
        hard_decline = True
    elif ai_score <= 0.70:
        needs_review = True
        
    if hard_decline:
        return DecisionResponse(
            decision="decline",
            interest_rate=0.0,
            ai_score=ai_score,
            reason_trail=reason_trail,
        )
    
    if needs_review:
        return DecisionResponse(
            decision="refer",\
            interest_rate=9.5,
            ai_score=ai_score,
            reason_trail=reason_trail,
        )
        
    interest_rate = 5.5 if ai_score >= 0.80 else 6.5
    return DecisionResponse(
        decision="approve",
        interest_rate=interest_rate,
        ai_score=ai_score,
        reason_trail=reason_trail,
    )