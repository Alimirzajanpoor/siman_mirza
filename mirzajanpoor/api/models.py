from django.db import models
import uuid


# Create your models here.


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(
        max_length=11, blank=True, null=True
    )  # maybe max lentgh?
    description = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# maybe storage type system?
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=30, blank=True, unique=True)
    price = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderQuerySet(models.QuerySet):
    def with_related(self):
        return self.select_related("customer").prefetch_related(
            "orderitem_set__product"
        )

    def by_customer(self, customer_id):
        return self.filter(customer_id=customer_id)


# next task
# add a buisness logic that with a state on_going , shipped , etc ...
# and possible implementation of labor in order to see which labor is responsible for each order
# add address logic to order for where its shipped
class Order(models.Model):
    objects = OrderQuerySet.as_manager()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=30, blank=True, unique=True)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="orders",
    )

    products = models.ManyToManyField(
        Product,
        related_name="orders",
        through="OrderItem",
    )
    total_price = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.title} × {self.quantity}"


class Labor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    national_code = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Labor_wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    labor = models.ForeignKey(Labor, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10,decimal_places=0)
    TRANSACTION_TYPE_CHOICES = {"CASH": "cash", "CARD": "card"}
    transaction_type = models.CharField(
        choices=TRANSACTION_TYPE_CHOICES, default="CASH"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
