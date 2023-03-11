from django.db import models


class Loan(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    term = models.IntegerField()
    name = models.CharField(max_length=255)
    personal_id = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
