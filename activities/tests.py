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

        # Create an activity for update tests
        self.activity = Activity.objects.create(
            user=self.user,
            activity_type="workout",
            description="Morning run",
            duration_minutes=45,
            calories=300
        )

    def test_list_activities(self):
        """Test retrieving all activities for the authenticated user"""
        url = reverse('activity-list')  # make sure this matches the URL name
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # Optional: check first activity fields
        self.assertEqual(response.data[0]['activity_type'], "workout")

    def test_create_activity(self):
        url = reverse('activity-list-create')
        data = {
            "activity_type": "meal",
            "description": "Breakfast - Oatmeal and eggs",
            "calories": 400
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 2)  # one created in setUp + this one
        self.assertEqual(Activity.objects.last().activity_type, "meal")

    def test_update_activity_status(self):
        """Test updating an existing activity's status"""
        url = reverse('activity-update', kwargs={'pk': self.activity.id})
        data = {
            "status": "completed",
            "description": "Morning run updated"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.activity.refresh_from_db()
        self.assertEqual(self.activity.status, "completed")
        self.assertEqual(self.activity.description, "Morning run updated")

    def test_delete_activity(self):
        """Test deleting an existing activity"""
        url = reverse('activity-delete', kwargs={'pk': self.activity.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Ensure the activity was actually deleted
        self.assertFalse(Activity.objects.filter(id=self.activity.id).exists())
