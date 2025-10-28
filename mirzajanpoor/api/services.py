from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from .models import Order, OrderItem, Product, Customer


@transaction.atomic
def create_order(*, customer_id, title, items_data):
    """
    Business logic for creating an order and related order items.
    """
    customer = Customer.objects.get(id=customer_id)

    order = Order.objects.create(customer=customer, title=title, total_price=0)
    total = 0

    for item_data in items_data:
        product = Product.objects.get(id=item_data["product_id"])
        quantity = item_data["quantity"]

        OrderItem.objects.create(order=order, product=product, quantity=quantity)
        total += product.price * quantity

    order.total_price = total
    order.save()
    return order


@transaction.atomic
def update_order(*, order_id, title, customer_id, items_data):
    try:
        order = (
            Order.objects.select_related("customer")
            .prefetch_related("orderitem_set__product")
            .get(id=order_id)
        )
    except Order.DoesNotExist:
        raise ValidationError("Order not found.")
    if title:
        order.title = title
    if customer_id:
        customer = Customer.objects.get(id=customer_id)
        order.customer = customer
    order.save()
    total_price = 0
    print(order.products.all(), type(order))
    existing_items = {item.product_id: item for item in order.orderitem_set.all()}

    if items_data:
        for item_data in items_data:
            action = item_data["action"]

            product = get_object_or_404(Product, id=item_data["product_id"])

            if action == "add":
                if product.id in existing_items:
                    raise ValidationError(f"Product {product.title} already in order.")
                quantity = item_data.get("quantity")
                if not quantity:
                    raise ValidationError(f"Quantity is required for 'add' action. ")
                OrderItem.objects.create(
                    order=order, product=product, quantity=quantity
                )
            elif action == "update":
                if product.id not in existing_items:
                    raise ValidationError(f"Product {product.title} not in this order.")
                if not quantity:
                    raise ValidationError("Quantity is required for 'update' action.")
                existing_items[product.id].quantity = quantity
                existing_items[product.id].save(update_fields=["quantity"])
            elif action == "remove":
                if product.id not in existing_items:
                    raise ValidationError(f"Product {product.title} not in this order.")
                existing_items[product.id].delete()
    for item in order.orderitem_set.select_related("product").all():
        total_price += item.product.price * item.quantity
        order.total_price = total_price
        order.save(update_fields=["total_price"])
    return order
