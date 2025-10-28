from rest_framework import serializers
from api.models import Customer, Product, Order, OrderItem
from django.db import transaction


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]


class ProductOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField()
    price = serializers.IntegerField()


class OrderItemOutputSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()
    product = ProductOutputSerializer()


class OrderOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField()
    first_name = serializers.CharField(source="customer.first_name")
    last_name = serializers.CharField(source="customer.last_name")
    total_price = serializers.IntegerField()
    items = serializers.SerializerMethodField(required=False)

    def get_items(self, obj: Order):

        order_items = obj.orderitem_set.all()
        return OrderItemOutputSerializer(order_items, many=True).data


class OrderItemInputSerializer(serializers.Serializer):
    ACTION_CHOICES = ["add", "update", "remove"]
    action = serializers.ChoiceField(choices=ACTION_CHOICES)
    product_id = serializers.UUIDField()
    quantity = serializers.IntegerField(required=False,min_value=1)
    def validate_product_id(self,value):
        from ..models import Product

        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("product not found")
        return value

class OrderInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=30,required=False)
    customer_id = serializers.UUIDField()
    items = OrderItemInputSerializer(many=True,required=False)

    def validate_title(self, value):
        if Order.objects.filter(title=value).exists():
            raise serializers.ValidationError(
                "An order with this title already exists."
            )
        return value

    def validate_customer_id(self, value):
        from ..models import Customer

        if not Customer.objects.filter(id=value).exists():
            raise serializers.ValidationError("Customer not found.")
        return value


# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True, write_only=True)
#     customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

#     class Meta:
#         model = Order
#         fields = [
#             "id",
#             "title",
#             "customer",
#             "items",
#             "created_at",
#             "updated_at",
#         ]
#         read_only_fields = ["id", "created_at", "updated_at", "total_price"]

#     def create(self, validated_data):
#         items_data = validated_data.pop("items")
#         with transaction.atomic():
#             order = Order.objects.create(**validated_data)
#             total = 0
#             for item_data in items_data:
#                 product = item_data["product"]
#                 quantity = item_data["quantity"]
#                 OrderItem.objects.create(
#                     order=order, product=product, quantity=quantity
#                 )
#                 total += product.price * quantity
#             order.total_price = total
#             order.save()

#         return order
