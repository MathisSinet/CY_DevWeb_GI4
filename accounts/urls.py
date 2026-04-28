from django.urls import path
from .views import *

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("modif/", modif_view, name="modif"),
    path("profile/", profile_view, name="profile"),
    path("verify_email/", verify_email_view, name="verify_email"),
    path("check_email/", check_email_view, name="check_email")
]