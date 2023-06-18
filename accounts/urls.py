from django.urls import include, path

from accounts.swagger.auth import (
    forger_password_endpoint,
    login_endpoint,
    logout_endpoint,
    register_endpoint,
    set_password_endpoint,
)
from accounts.swagger.connection import (
    create_connection_endpoint,
    update_connection_endpoint,
)
from accounts.swagger.profile import profiles_endpoint
from accounts.views.auth_views import (
    check_token,
    forget_password,
    login,
    logout,
    register,
    set_password,
)
from accounts.views.connection_views import connection, connections
from accounts.views.image_views import recognize_image
from accounts.views.profile_views import profiles

auth_urls = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("forget-password/", forget_password, name="forget-password"),
    path("check-token/<str:token>", check_token, name="check-token"),
    path("set-password/<str:token>", set_password, name="set-password"),
]
connection_urls = [
    path("", connections, name="connections"),
    path("<int:connection_id>", connection, name="connection"),
]
urlpatterns = [
    path("auth/", include(auth_urls)),
    path("profiles/", profiles, name="profile"),
    path("connections/", include(connection_urls)),
    path("recognize/", recognize_image, name="recognize image"),
]
