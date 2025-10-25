from rest_framework import generics, permissions
from .models import Activity
from .serializers import ActivitySerializer

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