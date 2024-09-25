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

    def test_create_order_price_over_limit(self):
        """Test that when order price exceeds 2000, it should return an error."""
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
        """Test that an invalid currency format should return an error."""
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

    def test_create_order_convert_usd_to_twd(self):
        """Test that when currency is USD, it is converted to TWD and multiplied by 31."""
        data = {
            "id": "A0000001",
            "name": "Melody Holiday Inn",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road"
            },
            "price": 50,
            "currency": "USD"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['price'], 50 * 31)  # Should multiply by 31
        self.assertEqual(response.data['currency'], "TWD")
