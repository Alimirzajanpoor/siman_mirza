from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import LaborViewSet

from .views import LaborViewSet, WalletLaborViewSet

router = DefaultRouter()

router.register(r"labors", LaborViewSet, basename="labor")
router.register(r"labor_wallet", WalletLaborViewSet, basename="labor_wallet")
urlpatterns = [
    path("", include(router.urls)),
    # path("labor-wallet/", LaborWalletCreateView.as_view()),
    # path("labor-wallets/", LaborWalletListView.as_view()),
    # path("orders/", OrderListView.as_view(), name="order-list"),
]
