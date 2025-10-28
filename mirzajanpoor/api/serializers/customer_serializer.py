from rest_framework import serializers
from api.models import Customer, Product, Order, OrderItem
from django.db import transaction


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = "__all__"
