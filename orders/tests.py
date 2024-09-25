from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class OrderAPITest(APITestCase):
    
    def setUp(self):
        # Set the URL name (assuming we configured the view in urls.py with the name 'orders')
        self.url = reverse('orders')

    def test_create_order_success(self):
        """Test successfully creating an order."""
        data = {
            "id": "A0000001",
            "name": "Melody Holiday Inn",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road"
            },
            "price": 1500,
            "currency": "TWD"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Melody Holiday Inn")
        self.assertEqual(response.data['price'], 1500)
        self.assertEqual(response.data['currency'], "TWD")

    def test_create_order_name_non_ascii(self):
        """Test order with a name containing non-ASCII characters should return error."""
        data = {
            "id": "A0000001",
            "name": "メロディ Holiday Inn",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road"
            },
            "price": 1500,
            "currency": "TWD"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Name contains non-English characters", response.data['name'])

    def test_create_order_name_not_capitalized(self):
        """Test order where the name's first letter is not capitalized should return error."""
        data = {
            "id": "A0000001",
            "name": "melody holiday inn",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road"
            },
            "price": 1500,
            "currency": "TWD"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Name is not capitalized", response.data['name'])

    def test_create_order_price_exceeds_limit(self):
        """Test order with a price exceeding 2000 should return error."""
        data = {
            "id": "A0000001",
            "name": "Melody Holiday Inn",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road"
            },
            "price": 2500,
            "currency": "TWD"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Price is over 2000", response.data['price'])

    def test_create_order_invalid_currency(self):
        """Test order with an invalid currency should return error."""
        data = {
            "id": "A0000001",
            "name": "Melody Holiday Inn",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road"
            },
            "price": 1500,
            "currency": "EUR"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Currency format is wrong", response.data['currency'])

    def test_create_order_success_with_usd(self):
        """Test successfully creating an order with USD currency should convert to TWD."""
        data = {
            "id": "A0000001",
            "name": "Melody Holiday Inn",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road"
            },
            "price": 100,  # USD
            "currency": "USD"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['price'], 3100)  # Converted price
        self.assertEqual(response.data['currency'], "TWD")

    def test_create_order_missing_fields(self):
        """Test order with missing required fields should return error."""
        data = {
            "name": "Melody Holiday Inn",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road"
            }
            # Missing 'id', 'price', and 'currency'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This field is required.", response.data['id'])
        self.assertIn("This field is required.", response.data['price'])
        self.assertIn("This field is required.", response.data['currency'])
