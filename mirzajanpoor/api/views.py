from django.shortcuts import render
from api.models import Customer, Product, Order
from api.serializers.customer_serializer import CustomerSerializer
from api.serializers.product_serializer import ProductSerializer
from api.serializers.order_serializer import OrderOutputSerializer, OrderInputSerializer
from rest_framework import viewsets, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from api import selectors
from api import services
from rest_framework.response import Response


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["first_name", "last_name", "phone_number"]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]


class OrderViewSet(viewsets.ModelViewSet):
    # filter_backends=[DjangoFilterBackend]
    # filterset_fields=[]
    filter_backends = [filters.SearchFilter]
    search_fields = search_fields = [
        "title",
        "customer__first_name",
        "customer__last_name",
    ]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return OrderInputSerializer
        return OrderOutputSerializer

    # def get_queryset(self):
    #     return selectors.get_orders()

    def get_queryset(self):
        queryset = selectors.get_orders(self.request.query_params)
        return queryset

    # def list(self, request, *args, **kwargs):
    #     queryset = selectors.get_orders(request.query_params)
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    def perform_create(self, serializer):
        validated = serializer.validated_data
        order = services.create_order(
            customer_id=validated["customer_id"],
            title=validated["title"],
            items_data=validated["items"],
        )
        return order

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = self.perform_create(serializer)
        output_serializer = OrderOutputSerializer(order)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer, partial=False):
        validated = serializer.validated_data
        order_id = self.kwargs["pk"]
        order = services.update_order(
            order_id=order_id,
            title=validated["title"],
            customer_id=validated["customer_id"],
            items_data=validated.get("items", None),
        )
        return order

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = self.perform_update(serializer)
        output_serializer = OrderOutputSerializer(order)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        """
        PATCH — delegate to DRF's default behavior
        (automatic field-based update via serializer.save()).
        """
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)
