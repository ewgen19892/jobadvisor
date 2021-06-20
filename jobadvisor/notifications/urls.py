"""Notifications URL Configuration."""
from django.urls import path

from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

from jobadvisor.notifications.views import MessageList, MessageRead

app_name: str = "notifications"
urlpatterns: list = [
    path("devices/", FCMDeviceAuthorizedViewSet.as_view({"post": "create"}),
         name="fcm_devices"),
    path("messages/", MessageList.as_view(), name="message_list"),
    path("messages/<int:pk>/", MessageRead.as_view(), name="message_read"),
]
