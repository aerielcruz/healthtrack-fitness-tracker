from rest_framework import serializers
from .models import Activity

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'activity_type', 'description', 'duration_minutes', 'calories', 'steps', 'status', 'date']
        read_only_fields = ['id', 'user', 'date']
