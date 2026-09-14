import json

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from order.factories import UserFactory
from product.factories import CategoryFactory, ProductFactory
from product.models import Product


class TestProductViewSet(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        self.token = Token.objects.create(user=self.user)

        self.category = CategoryFactory()
        self.product = ProductFactory(
            title="pro controller",
            price=200,
            category=[self.category],
        )

    def test_get_all_product(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(
            reverse("product-list", kwargs={"version": "v1"})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        product_data = json.loads(response.content)
        self.assertEqual(
            product_data["results"][0]["title"], self.product.title
        )
        self.assertEqual(
            product_data["results"][0]["price"], self.product.price
        )

    def test_create_product(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        category = CategoryFactory()
        data = json.dumps(
            {
                "title": "notebook",
                "price": 800,
                "categories_id": [category.id],
            }
        )

        response = self.client.post(
            reverse("product-list", kwargs={"version": "v1"}),
            data=data,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        created_product = Product.objects.get(title="notebook")
        self.assertEqual(created_product.title, "notebook")
        self.assertEqual(created_product.price, 800)
