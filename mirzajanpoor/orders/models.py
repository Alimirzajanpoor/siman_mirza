# apps/orders/models.py
from django.db import models
import uuid


class OrderQuerySet(models.QuerySet):
    def with_related(self):
        return self.select_related("customer").prefetch_related(
            "orderitem_set__product"
        )

    def by_customer(self, customer_id):
        return self.filter(customer_id=customer_id)


# Possible implemention of Quee?
class Order(models.Model):
    objects = OrderQuerySet.as_manager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=30, blank=True, unique=True)

    class StateChoices(models.TextChoices):
        LOADING = "loading", "Loading Order"
        SHIPPED = "shipped", "Shipped Order"
        DELIVERED = "delivered", "Delivered Order"
        PROCESSING = "processing", "Procsessing Order"
        HALTED = "halted", "Halted Order"

    state = models.CharField(
        choices=StateChoices.choices, default=StateChoices.PROCESSING
    )
    address = models.CharField(max_length=300, null=True)
    customer = models.ForeignKey(
        "customers.Customer",  # ✅ String reference!
        on_delete=models.CASCADE,
        related_name="orders",
    )

    products = models.ManyToManyField(
        "products.Product",  # ✅ String reference!
        related_name="orders",
        through="OrderItem",
    )

    total_price = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "orders"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order {self.title} - {self.customer}"


class OrderItem(models.Model):
    # Within same app - no string needed (but you can use strings)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    # Cross-app reference - use string
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE  # ✅ String reference!
    )

    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = "order_items"
        unique_together = ["order", "product"]  # Prevent duplicate items

    def __str__(self):
        return f"{self.product.title} × {self.quantity}"
