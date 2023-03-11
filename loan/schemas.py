from typing import List, Dict, Union
from datetime import datetime
from pydantic import BaseModel, condecimal


class LoanApplicationRequestSchema(BaseModel):
    amount: condecimal(max_digits=10, decimal_places=2)
    term: int
    name: str
    personal_id: str


class LoanApplicationResponseSchema(BaseModel):
    status: str
    monthly_repayment_amount: condecimal(max_digits=10, decimal_places=2) = None
    reason: str = None


class LoanListResponseSchema(BaseModel):
    loans: List[Dict[str, Union[condecimal(max_digits=10, decimal_places=2), int, str, datetime]]]
