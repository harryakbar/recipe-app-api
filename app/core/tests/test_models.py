from django.test import TestCase
from django.contrib.auth import get_user_model


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
            get_user_model().objects.create_user(None, 'password123')

    def test_create_super_user(self):
        """Test creating super user"""
        email = "harryakbaram@gmail.com"
        password = "password123"
        user = get_user_model().objects.create_superuser(
            email,
            password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
