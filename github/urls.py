from django.urls import path, include
from .views import webhook_post

urlpatterns = (
    path("webhook", webhook_post),
)
