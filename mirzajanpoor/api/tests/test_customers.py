from django.test import TestCase
from api.models import Customer


class CustomerTestCase(TestCase):
    def setUp(self):
        # Create some customers
        Customer.objects.create(
            first_name="Ali",
            last_name="Mirzajanpoor",
            phone_number=912345678,
            description="Test customer one",
        )
        Customer.objects.create(
            first_name="Sara",
            last_name="Ahmadi",
            phone_number=935678912,
            description="Test customer two",
        )

    def test_customer_creation(self):
        # Test count
        self.assertEqual(Customer.objects.count(), 2)

        # Fetch one customer
        customer = Customer.objects.get(first_name="Ali")
        self.assertEqual(customer.last_name, "Mirzajanpoor")
        self.assertEqual(customer.phone_number, 912345678)

    def test_customer_str_fields_blank_allowed(self):
        # Create a customer with blank fields (since blank=True)
        c = Customer.objects.create()
        self.assertIsInstance(c, Customer)
        self.assertEqual(c.first_name, "")
        self.assertEqual(c.last_name, "")

    def test_delete_customer(self):
        # Ensure the customer exists
        self.assertEqual(Customer.objects.count(), 2)

        # Delete one customer
        Customer.objects.filter(first_name="Ali").delete()

        # Check count after deletion
        self.assertEqual(Customer.objects.count(), 1)
        self.assertFalse(Customer.objects.filter(first_name="Ali").exists())


    def test_update_customer(self):
        customer = Customer.objects.get(first_name="Ali")
        customer.last_name = "UpdatedName"
        customer.save()

        updated_customer = Customer.objects.get(first_name="Ali")
        self.assertEqual(updated_customer.last_name, "UpdatedName")
