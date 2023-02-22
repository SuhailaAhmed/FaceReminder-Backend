from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from accounts.views.connection_views import create_connection

create_connection_endpoint = swagger_auto_schema(
    method= 'Post',
    request_body= openapi.Schema(type=openapi.TYPE_OBJECT, required= ['name', 'relation'], 
    properties={
        "name": openapi.Schema(type=openapi.TYPE_STRING, description="name of relative"),
        "relation": openapi.Schema(type=openapi.TYPE_STRING, description="relation of relative"),
        "age": openapi.Schema(type=openapi.TYPE_STRING, description="age of relative"),
        "address": openapi.Schema(type=openapi.TYPE_STRING, description="address of relative"),
        "biography": openapi.Schema(type=openapi.TYPE_STRING, description="biography of relative"),
    }
    ),
    responses={200: openapi.Response("Realtive added successfully")}
)(create_connection)