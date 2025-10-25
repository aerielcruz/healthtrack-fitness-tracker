from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Activity

class ActivityTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="activityuser@example.com",
            first_name="Test",
            last_name="User",
            password="password123"
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_activity(self):
        url = reverse('activity-list-create')
        data = {
            "activity_type": "workout",
            "description": "Morning run",
            "duration_minutes": 45,
            "calories": 300
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)
        self.assertEqual(Activity.objects.first().activity_type, "workout")
