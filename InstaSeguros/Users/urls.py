from django.contrib import admin
from django.urls import path, include
from .views import UserView

urlpatterns = [
    path("", UserView.as_view(), name="user_view"),
    path("<int:pk>/", UserView.as_view(), name="user_view_param"),
]
