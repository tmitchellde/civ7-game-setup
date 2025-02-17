from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),  # Django Admin Panel
    path("api/", include("picker.urls")),  # ✅ Ensure this line is present
]
