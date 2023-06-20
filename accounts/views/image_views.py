import os

from django.core.files.storage import default_storage
from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

from accounts.face_recognition import recognized
from accounts.serializers.image_serializer import ImageSerializer
from Gp_Backend import settings


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
@parser_classes([FormParser, MultiPartParser, JSONParser])
def recognize_image(request):
    body = request.data
    image_serialzer = ImageSerializer(data=body)

    image_serialzer.is_valid(raise_exception=True)
    image = image_serialzer.validated_data["image"]

    image_name = default_storage.save(image.name, image)

    image_url = f"\media\{image_name}"
    image_path = f"{settings.BASE_DIR}{image_url}"
    print("base DIR: ", settings.BASE_DIR)
    print("image_path: ", image_path)
    print(settings.FOLDER1_PATH)

    recognized_connection = recognized(image_path, settings.FOLDER1_PATH)

    return JsonResponse({"res": recognized_connection}, status=200, safe=False)
