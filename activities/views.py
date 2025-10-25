from rest_framework import generics, permissions
from .models import Activity
from .serializers import ActivitySerializer

class ActivityListView(generics.ListAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return all activities for the logged-in user
        return Activity.objects.filter(user=self.request.user).order_by('-date')

class ActivityListCreateView(generics.ListCreateAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ActivityUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Limit updates to current user's activities only
        return Activity.objects.filter(user=self.request.user)

class ActivityDeleteView(generics.RetrieveDestroyAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Limit deletes to current user's activities only
        return Activity.objects.filter(user=self.request.user)
