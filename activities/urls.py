from django.urls import path
from .views import ActivityListCreateView, ActivityUpdateView, ActivityDeleteView

urlpatterns = [
    path('activities/', ActivityListCreateView.as_view(), name='activity-list-create'),
    path('activities/<int:pk>/', ActivityUpdateView.as_view(), name='activity-update'),
    path('activities/<int:pk>/delete', ActivityDeleteView.as_view(), name='activity-delete'),
]
