from django.shortcuts import render
from .models import Product
from .serializer import ProductSerializer

from rest_framework import viewsets, status, filters



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]
