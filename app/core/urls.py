from django.urls import path

from .views import (
    HomePageView,
    RegisterView,
    LoginView,
    LogoutView,
    URLCreateView,
    URLDeleteView,
    URLUpdateView,
    RedirectURLView,
    StatsPageView,
)


app_name = "core"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("createURL/", URLCreateView.as_view(), name="create-url"),
    path("deleteURL/<str:shortened_url>", URLDeleteView.as_view(), name="delete-url"),
    path("updateURL/<str:shortened_url>", URLUpdateView.as_view(), name="update-url"),
    path("<str:shortened_url>", RedirectURLView.as_view(), name="redirect"),
    path("stats/", StatsPageView.as_view(), name="stats"),

]
