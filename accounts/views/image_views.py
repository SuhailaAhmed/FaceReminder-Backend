import os

from django.core.files.storage import default_storage
from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

from accounts.face_recognition import recognized
from accounts.models.connection import Connection
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

    account_id = request.user.id

    recognized_connection = recognized(image_path, f"{settings.FOLDER1_PATH}\{account_id}")

    if recognized_connection:
        filename = os.path.basename(recognized_connection)
        try:
            connection = Connection.objects.get(image__endswith=filename)
            connection_id = connection.id
            return JsonResponse({"result": connection_id}, status=200, safe=False)

        except Connection.DoesNotExist:
            return JsonResponse({"error": "Connection not found for the given image name."}, status=400, safe=False)

    else:
        return JsonResponse({"result": recognized_connection}, status=201, safe=False)
