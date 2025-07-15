from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class ProductListViewTest(TestCase):
    def test_product_list_status_code(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
