from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from accounts.face_recognition import recognized
from Gp_Backend.s3_storages import MediaStorage


def upload_image(image, image_path):
    storage = MediaStorage()
    storage.save(image_path, image)


@api_view(
    [
        "POST",
    ]
)
@permission_classes(
    [
        IsAuthenticated,
    ]
)
def recognize_image(request):
    image = request.data.get("image", None)

    if not image:
        return JsonResponse({"error": "missing `image`"}, status=400)

    filename = image.name
    image_path = f"recognition/{filename}"
    upload_image(image, image_path)

    folder_path = f"connections/"

    recognized_connection = recognized(image_path, folder_path)
    return recognized_connection


@permission_classes(
    [
        IsAuthenticated,
    ]
)
def check_image(request):
    image = request.data.get("image", None)

    if not image:
        return True
    else:
        False
