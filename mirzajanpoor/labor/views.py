from .models import Labor, Labor_wallet
from .service import LaborWalletService
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .serializer import (
    LaborSerializer,
    LaborWalletSerializer,
    LaborWalletOutputSerializer,
    LaborWalletInputSerializer,
)
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.response import Response


class LaborViewSet(viewsets.ModelViewSet):
    queryset = Labor.objects.all()
    serializer_class = LaborSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["first_name", "last_name"]


class WalletLaborViewSet(viewsets.ModelViewSet):
    queryset = Labor_wallet.objects.all()
    serializer_class = LaborWalletSerializer

    # looks intresting maybe using this logic later....
    # @action(detail=True, methods=["post"], url_path="wallet/deposit")
    # def deposit(self, request, pk=None):
    #     labor = self.get_object()
    #     serializer = LaborWalletInputSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     # Use your service
    #     instance = LaborWalletService.create_labor_wallet(
    #         labor_id=labor.id,
    #         amount=serializer.validated_data["amount"],
    #         transaction_type=Labor_wallet.TransactionType.DEPOSIT,
    #     )
    #     return Response(LaborWalletOutputSerializer(instance).data, status=201)

    # @action(detail=True, methods=["post"], url_path="wallet/withdraw")
    # def withdraw(self, request, pk=None):
    #     labor = self.get_object()
    #     serializer = LaborWalletInputSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     instance = LaborWalletService.create_labor_wallet(
    #         labor_id=labor.id,
    #         amount=serializer.validated_data["amount"],
    #         transaction_type=Labor_wallet.TransactionType.WITHDRAWAL,
    #     )
    #     return Response(LaborWalletOutputSerializer(instance).data, status=201)


# class LaborWalletCreateView(generics.CreateAPIView):
#     serializer_class = LaborWalletInputSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         data = serializer.validated_data
#         instance = LaborWalletService.create_labor_wallet(**data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# class LaborWalletListView(generics.ListAPIView):
#     # serializer_class = LaborWalletOutputSerializer
#     def get_queryset(self):
#         return Labor_wallet.objects.all()

#     def list(self, request):
#         queryset = self.get_queryset()
#         serializer = LaborWalletOutputSerializer(queryset, many=True)
#         return Response(serializer.data)
