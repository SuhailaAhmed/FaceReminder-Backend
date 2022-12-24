from django.urls import path, include
from accounts.views.auth_views import register, login, logout, forget_password,check_token,set_password
from accounts.swagger import register_endpoint, login_endpoint, logout_endpoint, forger_password_endpoint, set_password_endpoint

auth_urls = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('forget-password/', forget_password, name="forget-password" ),
    path('check-token/<str:token>', check_token, name='check-token'),
    path('set-password/<str:token>', set_password, name='set-password'),
]

urlpatterns = [
    path('auth/', include(auth_urls)),
]