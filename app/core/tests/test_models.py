from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email="test@gmail.com", password="testpass"):
    """Create simple user"""
    return get_user_model().objects.create(email=email, password=password)


class ModelTests(TestCase):
    def test_create_with_email_successful(self):
        """Test Creating a new user with an email is successful"""
        email = "harryakbaram@gmail.com"
        password = "password123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_with_normalized_email(self):
        """Test Creating a new user with an email is normalized"""
        email = "harryakbaram@GMAIL.com"
        password = "password123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email.lower())
        self.assertTrue(user.check_password(password))

    def test_create_with_email_invalid(self):
        """Test Creating a new user with an email is invalid"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "password123")

    def test_create_super_user(self):
        """Test creating super user"""
        email = "harryakbaram@gmail.com"
        password = "password123"
        user = get_user_model().objects.create_superuser(email, password)

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test tag string representation"""
        tag = models.Tag.objects.create(user=sample_user(), name="Vegan")

        self.assertEqual(str(tag), tag.name)

    def test_ingredients_str(self):
        """Test tag string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(), name="Cucumber"
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipes_str(self):
        """Test recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title="Rendang Balado",
            time_minutes=5,
            price=50_000_000
        )

        self.assertEqual(str(recipe), recipe.title)
