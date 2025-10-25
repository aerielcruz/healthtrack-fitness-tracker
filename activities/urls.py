from django.urls import path
from .views import ActivityListView, ActivityListCreateView, ActivityUpdateView, ActivityDeleteView

urlpatterns = [
    path('activities/list/', ActivityListView.as_view(), name='activity-list'),
    path('activities/', ActivityListCreateView.as_view(), name='activity-list-create'),
    path('activities/<int:pk>/', ActivityUpdateView.as_view(), name='activity-update'),
    path('activities/<int:pk>/delete', ActivityDeleteView.as_view(), name='activity-delete'),
]
