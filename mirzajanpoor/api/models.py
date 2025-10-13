from django.db import models
import uuid
# Create your models here.


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = models.IntegerField(max_length=11, blank=True)
    description= models.CharField(max_length=300,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=30, blank=True,unique=True)
    price=models.IntegerField(null=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=30, blank=True, unique=True)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,     # delete orders if customer is deleted
        related_name="orders",        # allows customer.orders.all()
    )

    products = models.ManyToManyField(
        Product,
        related_name="orders",        # allows product.orders.all()
        through="OrderItem",          # optional custom through model (see below)
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
