from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, Any

from django.conf import settings
from ninja import Router

from .models import Loan
from .schemas import LoanApplicationRequestSchema, LoanApplicationResponseSchema, LoanListResponseSchema

router = Router()


# Function to check if a personal ID is blacklisted
def is_blacklisted(personal_id: str) -> bool:
    return personal_id in settings.BLACKLISTED_IDS


# Function to check if there have been too many loan applications from a personal ID in the last 24 hours
def has_too_many_applications(personal_id: str) -> bool:
    last_24_hours = datetime.now() - timedelta(hours=24)
    recent_applications = Loan.objects.filter(personal_id=personal_id, created_at__gte=last_24_hours)
    return recent_applications.count() >= settings.MAX_APPLICATIONS_PER_DAY


@router.post('/loan', response=LoanApplicationResponseSchema)
def apply_loan(request, loan_request: LoanApplicationRequestSchema) -> Dict[str, Any]:
    personal_id = loan_request.personal_id
    if is_blacklisted(personal_id):
        return {'status': 'rejected', 'reason': 'blacklisted'}

    if has_too_many_applications(personal_id):
        return {'status': 'rejected', 'reason': 'too many applications'}

    amount = loan_request.amount
    term = loan_request.term
    interest_rate = Decimal(0.05)
    monthly_repayment_amount = Decimal((amount * interest_rate / 1200) / (1 - (1 + interest_rate / 1200) ** (-term)))

    loan = Loan.objects.create(
        personal_id=personal_id,
        name=loan_request.name,
        amount=amount,
        term=term,
        monthly_repayment_amount=monthly_repayment_amount,
        interest_rate=interest_rate,
    )

    return {'status': 'approved', 'monthly_repayment_amount': float(monthly_repayment_amount), 'loan': loan.id}


@router.get('/loans/{personal_id}', response=LoanListResponseSchema)
def list_loans(request, personal_id: str) -> Dict[str, Any]:
    loans = Loan.objects.filter(personal_id=personal_id).values(
        'amount', 'term', 'monthly_repayment_amount', 'created_at'
    )
    if not loans:
        return {'status': 'rejected', 'reason': 'no loans found'}
    return {'status': 'approved', 'loans': list(loans)}
