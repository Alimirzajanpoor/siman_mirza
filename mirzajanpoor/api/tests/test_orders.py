from api.models import Order,Customer
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from api.models import Customer, Product, Order

class OrderAPITest(APITestCase):
    def setUp(self):
        # Create some test data
        self.customer = Customer.objects.create(first_name="Ali", last_name="Mirza")
        self.product1 = Product.objects.create(title="گچ آزادی", price=2500)
        self.product2 = Product.objects.create(title="گچ سمنان", price=1000)

        # URL for the order endpoint (depends on your router)
        self.url = reverse("order-list")  # Usually from DRF router

    def test_create_order(self):
        payload = {
            "title": "My First Order",
            "customer": self.customer.id,
            "items": [
                {"product": self.product1.id, "quantity": 2},
                {"product": self.product2.id, "quantity": 1},
            ],
        }

        response = self.client.post(self.url, payload, format="json")

        # Assert the request succeeded
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert the order was created
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.total_price, 2500 * 2 + 1000 * 1)

        # Assert items were created
        self.assertEqual(order.items.count(), 2)
