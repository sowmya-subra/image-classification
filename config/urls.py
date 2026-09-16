from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from classifier import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", views.classify, name="classify"),
    path("writeup/", views.writeup, name="writeup"),
]