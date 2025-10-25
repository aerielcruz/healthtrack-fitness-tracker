from django.urls import path
from .views import ActivityListCreateView, ActivityUpdateView

urlpatterns = [
    path('activities/', ActivityListCreateView.as_view(), name='activity-list-create'),
    path('activities/<int:pk>/', ActivityUpdateView.as_view(), name='activity-update'),
]
