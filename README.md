# Loan Decision API

A lightweight FastAPI microservice that evaluates mock loan applications using deterministic business rules and a AI risk score, returning an `approve`, `decline`, or `refer` decision alongside a transparent `reason_trail`.

## Project Structure

```text
decision-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI routes (/health, /decision)
│   ├── schemas.py       # Pydantic request/response models & validation
│   └── decision.py      # Business rules, stubbed AI score & reason trail
├── tests/
│   ├── __init__.py
│   └── test_decision.py # Automated pytest suite
├── requirements.txt
└── README.md
```

## Decision Logic

1. **Rule 1 – Employment Check:** Flags unemployed applicants for manual review (`refer`).
2. **Rule 2 – Affordability:** Declines applications if estimated monthly repayment (`amount / term_months`) exceeds 40% of net monthly income.
3. **Rule 3 – Collateral Requirement:** Flags loans above `50,000` for manual review if collateral value is below 50% of the requested amount.
4. **Stubbed AI Risk Score:** Computes a deterministic score (`0.0` – `1.0`) based on employment, collateral ratio, and payment-to-income ratio (`>= 0.70` required for auto-approval).

## Setup & Local Run

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Start the development server
uvicorn app.main:app --reload
```

Interactive API documentation (Swagger UI) is available at `http://127.0.0.1:8000/docs`.

## Running Tests

```bash
pytest -v
```

## Example Request (`POST /decision`)

```json
{
  "amount": 10000,
  "term_months": 24,
  "is_employed": true,
  "monthly_income": 3000,
  "collateral_value": 0
}
```

### Example Response

```json
{
  "decision": "approve",
  "interest_rate": 5.5,
  "ai_score": 0.8,
  "reason_trail": [
    "Rule 1 (Employment): Passed - applicant is currently employed",
    "Rule 2 (Affordability): Passed - estimated payment (416.67) is within 40% of monthly income",
    "Rule 3 (Collateral): Passed - loan amount and collateral are within limits",
    "AI Risk Score: 0.80 (auto-approve threshold >= 0.70)"
  ]
}
```

## AWS Serverless Deployment Notes

Because `app/decision.py` and `app/schemas.py` are completely decoupled from the HTTP transport layer, this service can be deployed to **AWS Lambda + API Gateway** with minimal changes:

* Wrap the FastAPI `app` instance with **`Mangum`** (`handler = Mangum(app)`) in `app/main.py` to translate API Gateway events into ASGI requests.
* Package the function via AWS SAM, Serverless Framework, or a lightweight container image on AWS ECR.