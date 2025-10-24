from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

class UserAPITests(APITestCase):
    def setUp(self):
        # Create a user for testing login and authenticated endpoints
        self.user = User.objects.create_user(
            email="testuser@example.com",
            first_name="Test",
            last_name="User",
            password="password123"
        )

    def test_register_user(self):
        """Test user registration via RegisterView"""
        url = reverse('register')  # make sure your urls.py has name='register'
        data = {
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "newpassword123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())
