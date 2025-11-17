from django.db import models
import uuid

class Labor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    national_code = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Labor_wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    labor = models.ForeignKey(Labor, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=0)

    class TransactionType(models.TextChoices):
        CASH = "cash", "Cash Payment"  # (db_value, human_readable)
        CARD = "card", "Card Payment"
        BANK_TRANSFER = "bank_transfer", "Bank Transfer"

    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionType.choices,
        default=TransactionType.CASH,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
