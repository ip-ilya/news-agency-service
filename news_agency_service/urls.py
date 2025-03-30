from django.contrib import admin
from django.urls import path, include
from news_agency.views import CustomLoginView
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("news_agency.urls", namespace="news_agency")),
    path("accounts/login/", CustomLoginView.as_view(), name="login"),
    path("accounts/", include("django.contrib.auth.urls"))
]
