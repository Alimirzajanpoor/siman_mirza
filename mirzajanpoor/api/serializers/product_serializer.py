from rest_framework import serializers
from api.models import Customer, Product, Order, OrderItem
from django.db import transaction


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
            