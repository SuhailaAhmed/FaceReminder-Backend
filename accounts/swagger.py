from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from accounts.views import register, login, logout

register_endpoint = swagger_auto_schema(
    method= 'Post',
    request_body= openapi.Schema(type=openapi.TYPE_OBJECT, 
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
    request_body= openapi.Schema(type=openapi.TYPE_OBJECT, 
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