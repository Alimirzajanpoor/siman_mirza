from django.test import TestCase
from api.models import Product


class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(title="گچ آزادی", price=2500)
        
        Product.objects.create(title="گچ سمنان", price=1000)

    def test_Products_db(self):

        prod1 = Product.objects.get(title="گچ آزادی")
        prod2 = Product.objects.get(title="گچ سمنان")
        self.assertEqual(prod1.price, 2500)
        self.assertEqual(prod2.price, 1000)
