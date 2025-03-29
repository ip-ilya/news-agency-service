from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("news_agency.urls", namespace="news_agency")),
    path("accounts/", include("django.contrib.auth.urls"))
]
