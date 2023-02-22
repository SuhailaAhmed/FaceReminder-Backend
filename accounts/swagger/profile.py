from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from accounts.views.profile_views import profiles

profiles_endpoint = swagger_auto_schema(
    method= 'patch',
    request_body= openapi.Schema(type=openapi.TYPE_OBJECT,
    properties={
        "fullname": openapi.Schema(type=openapi.TYPE_STRING, description="Fullname of user"),
        "phone": openapi.Schema(type=openapi.TYPE_STRING, description="Phone Number of user"),
        "address": openapi.Schema(type=openapi.TYPE_STRING, description="Address of user"),
        "image": openapi.Schema(type=openapi.TYPE_STRING, description="Image of user"),
    }
    ),
    responses={200: openapi.Response("Account updated sucessfully")}
)(profiles)