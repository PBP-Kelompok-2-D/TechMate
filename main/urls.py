from django.urls import path
from main.views import (
    show_main,
    show_user_profile,
    edit_user_profile,
    register,
    login_user,
    logout_user,
)

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('profile/<uuid:profile_id>/', show_user_profile, name='show_user_profile'),
    path('profile/<uuid:profile_id>/edit/', edit_user_profile, name='edit_user_profile'),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
]