from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializers

RECIPES_URL = reverse("recipe:recipe-list")


class PublicRecipeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "test@gmail.com", "password123"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        Recipe.objects.create(
            title="Nasi Goreng", user=self.user, time_minutes=12, price=20000
        )
        Recipe.objects.create(
            title="Mie Goreng", user=self.user, time_minutes=10, price=20000
        )

        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all().order_by("-id")
        serializers = RecipeSerializers(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(serializers.data, res.data)

    def test_recipes_limited_to_users(self):
        user2 = get_user_model().objects.create_user(
            "other@gmail.com",
            "testpass",
        )
        Recipe.objects.create(
            title="Dendeng Balado", user=user2, time_minutes=12, price=230000
        )
        recipe = Recipe.objects.create(
            title="Nasi Goreng", user=self.user, time_minutes=12, price=20000
        )

        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["id"], recipe.id)

    def test_create_recipe(self):
        payload = {
            "title": "Nasi Goreng",
            "time_minutes": 23,
            "price": 23000,
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.filter(id=res.data["id"]).first()
        for key in payload:
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_create_recipe_invalid(self):
        payload = {
            "title": "",
            "time_minutes": 23,
            "price": 23000,
        }
        res = self.client.post(RECIPES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
