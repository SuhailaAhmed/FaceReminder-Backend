from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema

from accounts.views.image_views import preview_image, recognize_image

recognize_image_endpoint = swagger_auto_schema(
    method="Post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["image"],
        properties={
            "image": openapi.Schema(type=openapi.TYPE_STRING, description="recognized image"),
        },
    ),
    responses={200: openapi.Response("Image Recognized successfuly")},
)(recognize_image)

preview_image_endpoint = swagger_auto_schema(
    method="Get",
    responses={200: openapi.Response("Preview Image")},
)(preview_image)
