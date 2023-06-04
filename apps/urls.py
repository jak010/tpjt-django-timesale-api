from django.urls import path

from .views import (
    greeting
)

urlpatterns = [
    path("^$", greeting.GreetingView.as_view()),
]
