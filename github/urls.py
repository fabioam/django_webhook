from django.urls import path, include
from . import views

urlpatterns = (
    path("webhook", views.webhook_post),
    # path("webhook-test", views.webhook_post_test),
)
