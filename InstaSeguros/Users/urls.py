from django.contrib import admin
from django.urls import path, include
from .views import UserView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("", UserView.as_view()),
    path("<int:pk>", UserView.as_view()),
]
