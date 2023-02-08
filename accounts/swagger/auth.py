from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from accounts.views.auth_views import register, login, logout, forget_password, set_password

register_endpoint = swagger_auto_schema(
    method= 'Post',
    request_body= openapi.Schema(type=openapi.TYPE_OBJECT, required=['fullname', 'email', 'password', 'confirm_password'], 
    properties={
        "fullname": openapi.Schema(type=openapi.TYPE_STRING, description="Full Name of user"),
        "email": openapi.Schema(type=openapi.TYPE_STRING, description="Email of user"),
        "password": openapi.Schema(type=openapi.TYPE_STRING, description="Password of user"),
        "confirm_password": openapi.Schema(type=openapi.TYPE_STRING, description="Confirm Password of user"),
    }
    ),
    responses={200: openapi.Response("Account created sucessfully")}
)(register)


login_endpoint = swagger_auto_schema(
    method= 'Post',
    request_body= openapi.Schema(type=openapi.TYPE_OBJECT, required=['email', 'password'],
    properties={
        "email": openapi.Schema(type=openapi.TYPE_STRING, description="Email of user"),
        "password": openapi.Schema(type=openapi.TYPE_STRING, description="Password of user"),
    }
    ),
    responses={200: openapi.Response("Account logged in sucessfully")}
)(login)


logout_endpoint = swagger_auto_schema(
    method= 'Get',
    responses={200: openapi.Response("Account logged out sucessfully")}
)(logout)

forger_password_endpoint = swagger_auto_schema(
    method= 'Post',
    request_body= openapi.Schema(type=openapi.TYPE_OBJECT, required=['email'],
    properties={
        "email": openapi.Schema(type=openapi.TYPE_STRING, description="Email of user"),
    }
    ),
    responses={200: openapi.Response("Password reset link sent to your email")}
)(forget_password)

set_password_endpoint = swagger_auto_schema(
    method= 'Post',
    request_body= openapi.Schema(type=openapi.TYPE_OBJECT, required=['password', 'confirm_password'],
    properties={
        "password": openapi.Schema(type=openapi.TYPE_STRING, description="Password of user"),
        "confirm_password": openapi.Schema(type=openapi.TYPE_STRING, description="Confirm Password of user"),
    }
    ),
    responses={200: openapi.Response("Password reset sucessfully")}
)(set_password)