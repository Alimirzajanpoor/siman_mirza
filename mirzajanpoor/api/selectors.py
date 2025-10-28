from api.models import Order
from django.db.models import Prefetch
import django_filters

def get_orders(filters=None):

    queryset = Order.objects.select_related("customer").prefetch_related(
        "orderitem_set__product"
    )

    if filters:
        if customer_id := filters.get("customer_id"):
            queryset = queryset.filter(customer_id=customer_id)

    return queryset
