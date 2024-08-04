from django.contrib import admin
from django.urls import include, path
from decouple import config
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

base_url = config("BASE_URL")

urlpatterns = [
    path(
        "api_schema/",
        get_schema_view(
            title="InstaSeguros API",
            description="API for InstaSeguros",
            version="1.0",
        ),
        name="api_schema",
    ),
    path(
        "docs/",
        TemplateView.as_view(
            template_name="docs.html", extra_context={"schema_url": "api_schema"}
        ),
        name="swagger-ui",
    ),
    path("admin/", admin.site.urls),
    path(f"{base_url}/users/", include("Users.urls")),
]
