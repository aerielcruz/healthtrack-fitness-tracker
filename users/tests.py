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

    def test_login_user(self):
        """Test user login via JWT TokenObtainPairView"""
        url = reverse('token_obtain_pair')
        data = {
            "email": "testuser@example.com",
            "password": "password123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_user_invalid_credentials(self):
        """Test login fails with wrong credentials"""
        url = reverse('token_obtain_pair')
        data = {
            "email": "testuser@example.com",
            "password": "wrongpassword"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("access", response.data)

    def test_logout_user(self):
        """Test user logout with a valid refresh token"""
        # Step 1: Log in to get access and refresh tokens
        login_url = reverse('token_obtain_pair')
        login_data = {
            "email": "testuser@example.com",
            "password": "password123"
        }
        login_response = self.client.post(login_url, login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        access_token = login_response.data["access"]
        refresh_token = login_response.data["refresh"]

        # Step 2: Add Authorization header (required by IsAuthenticated)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        # Step 3: Logout with valid refresh token
        logout_url = reverse('logout')
        response = self.client.post(logout_url, {"refresh": refresh_token})
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_logout_user_invalid_token(self):
        """Test logout with invalid or missing refresh token"""
        # Must be authenticated
        login_url = reverse('token_obtain_pair')
        login_data = {
            "email": "testuser@example.com",
            "password": "password123"
        }
        login_response = self.client.post(login_url, login_data)
        access_token = login_response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        # Invalid refresh token
        logout_url = reverse('logout')
        response = self.client.post(logout_url, {"refresh": "invalidtoken"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
