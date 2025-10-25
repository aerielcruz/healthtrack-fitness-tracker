from django.db import models
from django.conf import settings

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('workout', 'Workout'),
        ('meal', 'Meal'),
        ('steps', 'Steps'),
    ]
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)  # for workouts
    calories = models.PositiveIntegerField(null=True, blank=True)          # for meals or workouts
    steps = models.PositiveIntegerField(null=True, blank=True)             # for steps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.activity_type} ({self.date})"
