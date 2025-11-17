from django.db import transaction
from .models import Labor, Labor_wallet
from .exceptions import (
    InsufficientBalanceError,
    InvalidTransactionError,
    WalletAlreadyExistsError,
)
from rest_framework import serializers
from rest_framework.generics import get_object_or_404


class LaborWalletService:
    @staticmethod
    @transaction.atomic
    def create_labor_wallet(*, labor_id, amount, transaction_type):
        labor = get_object_or_404(Labor, id=labor_id)
        # fetched_wallet=Labor_wallet.objects.get(labor_id=labor_id)

        labor_wallet = Labor_wallet.objects.create(
            labor_id=labor_id, amount=amount, transaction_type=transaction_type
        )

        labor_wallet.save()
        return labor
    