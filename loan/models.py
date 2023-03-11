from django.db import models
from decimal import Decimal


class Loan(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    term = models.IntegerField()
    name = models.CharField(max_length=255)
    personal_id = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    monthly_repayment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal(0.00))

    def save(self, *args, **kwargs):
        # Calculate the monthly repayment amount based on the amount, term and interest rate
        self.monthly_repayment_amount = Decimal(
            (self.amount * self.interest_rate / 1200) / (1 - (1 + self.interest_rate / 1200) ** (-self.term)))
        super().save(*args, **kwargs)
