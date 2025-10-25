from django.urls import path
from .views import ActivityListCreateView

urlpatterns = [
    path('activities/', ActivityListCreateView.as_view(), name='activity-list-create'),
]
