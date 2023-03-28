from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema

from accounts.views.connection_views import connections, update_connection

create_connection_endpoint = swagger_auto_schema(
    method="Post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["image"],
        properties={
            "image": openapi.Schema(type=openapi.TYPE_STRING, description="image of relative"),
            "name": openapi.Schema(type=openapi.TYPE_STRING, description="name of relative"),
            "relation": openapi.Schema(type=openapi.TYPE_STRING, description="relation of relative"),
            "age": openapi.Schema(type=openapi.TYPE_INTEGER, description="age of relative"),
            "address": openapi.Schema(type=openapi.TYPE_STRING, description="address of relative"),
            "biography": openapi.Schema(type=openapi.TYPE_STRING, description="biography of relative"),
        },
    ),
    responses={200: openapi.Response("Realtive added successfully")},
)(connections)

update_connection_endpoint = swagger_auto_schema(
    method="Patch",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "image": openapi.Schema(type=openapi.TYPE_STRING, description="image of relative"),
            "name": openapi.Schema(type=openapi.TYPE_STRING, description="name of relative"),
            "relation": openapi.Schema(type=openapi.TYPE_STRING, description="relation of relative"),
            "age": openapi.Schema(type=openapi.TYPE_INTEGER, description="age of relative"),
            "address": openapi.Schema(type=openapi.TYPE_STRING, description="address of relative"),
            "biography": openapi.Schema(type=openapi.TYPE_STRING, description="biography of relative"),
        },
    ),
    responses={200: openapi.Response("Realtive updated successfully")},
)(update_connection)
