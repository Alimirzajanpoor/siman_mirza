from django.shortcuts import render
from .models import Customer
from .serializer import CustomerSerializer

from rest_framework import viewsets, status, filters


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["first_name", "last_name", "phone_number"]
