import json

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from order.factories import UserFactory
from product.factories import ProductFactory


class TestPagination(APITestCase):
    client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        # PAGE_SIZE = 5 → cria 6 produtos para forçar uma segunda página
        self.products = [ProductFactory() for _ in range(6)]

    def test_product_list_is_paginated(self):
        response = self.client.get(
            reverse("product-list", kwargs={"version": "v1"})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)

        self.assertEqual(data["count"], 6)
        self.assertEqual(len(data["results"]), 5)
        self.assertIsNotNone(data["next"])
        self.assertIsNone(data["previous"])

    def test_product_list_second_page(self):
        response = self.client.get(
            reverse("product-list", kwargs={"version": "v1"}),
            {"page": 2},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = json.loads(response.content)

        self.assertEqual(data["count"], 6)
        self.assertEqual(len(data["results"]), 1)
        self.assertIsNone(data["next"])
        self.assertIsNotNone(data["previous"])
