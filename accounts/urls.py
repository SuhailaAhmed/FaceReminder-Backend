from django.urls import path
from accounts.views import register, login, logout
from accounts.swagger import register_endpoint, login_endpoint, logout_endpoint

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout')
]