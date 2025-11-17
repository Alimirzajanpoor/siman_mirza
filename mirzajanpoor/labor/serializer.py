from rest_framework import serializers
from .models import Labor, Labor_wallet
from django.db import transaction


class LaborSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labor
        fields = "__all__"


class LaborWalletSerializer(serializers.ModelSerializer):
    # labor = LaborSerializer(read_only=True)
    first_name = serializers.CharField(source="labor.first_name", read_only=True)
    last_name = serializers.CharField(source="labor.last_name", read_only=True)

    class Meta:
        model = Labor_wallet
        fields = "__all__"


class LaborWalletInputSerializer(serializers.Serializer):
    # id = serializers.UUIDField()
    labor_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = serializers.ChoiceField(
        choices=Labor_wallet.TransactionType.choices  # Must specify!
    )


class LaborWalletOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    labor_id = serializers.UUIDField(source="labor.id")  # Still include ID
    labor_name = serializers.CharField(source="labor.first_name")  # Just the name
    labor_last = serializers.CharField(source="labor.last_name")
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = serializers.ChoiceField(
        choices=Labor_wallet.TransactionType.choices  # Must specify!
    )
