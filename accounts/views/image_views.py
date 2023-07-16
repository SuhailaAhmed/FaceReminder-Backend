import base64
import os
import cv2

from django.core.files.storage import FileSystemStorage, default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

# from accounts.face_recognition import recognized
from accounts.copy_of_facenet_final_class import Facenet_find
from accounts.models.connection import Connection
from accounts.serializers.image_serializer import ImageSerializer
from Gp_Backend import settings
from Gp_Backend.settings import MEDIA_ROOT


@csrf_exempt
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
def upload(request):
    image_file = request.FILES.get("imageFile")
    account_id = request.user.id
    # Save the image file
    if image_file:
        file_path = os.path.join(f"{settings.FOLDER1_PATH}/{account_id}", "ESP32CAMCap.jpg")
        with open(file_path, "wb") as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)
        return JsonResponse({"message": "Image saved successfully.", "path":file_path})
    else:
        return JsonResponse({"message": "No image."})


@api_view(
    [
        "GET",
    ]
)
@permission_classes(
    [
        IsAuthenticated,
    ]
)
def preview_image(request):
    # Construct the file path for the requested image
    file_path = os.path.join(MEDIA_ROOT, "ESP32CAMCap.jpg")
    # Check if the image file exists
    if os.path.exists(file_path):
        with open(file_path, "rb") as image_file:
            # Read the image file as bytes
            image_data = image_file.read()
            # Encode the image data as Base64
            base64_image = base64.b64encode(image_data).decode("utf-8")

            # Return the Base64 encoded image in the response
            return JsonResponse({"image": base64_image})
    else:
        return JsonResponse({"error": "Image not found."}, status=404)
    
def resize_img(current_img):
  
  factor_0 = 512 / len(current_img[0])
  factor_1 = 512 / len(current_img[1])
  factor = min(factor_0, factor_1)

  dsize = (int(current_img.shape[1] * factor), int(current_img.shape[0] * factor))
  current_img = cv2.resize(current_img, dsize)
  return current_img

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

    image_path = os.path.join(MEDIA_ROOT, image_name)

    account_id = request.user.id

    img = cv2.imread(image_path)

    image_resized = resize_img(img)
    print(settings.BASE_DIR)
    print(settings.FOLDER1_PATH)
    print(f"{settings.FOLDER1_PATH}/{account_id}")
    recognized_connection, rep = Facenet_find(image_resized, f"{settings.FOLDER1_PATH}/{account_id}")

    if os.path.exists(image_path):
        os.remove(image_path)
        print("Image deleted successfully.")
    else:
        print("Image does not exist.")

    if recognized_connection == "no face detected":
        return JsonResponse({"error": "Can't detect face from this image."}, status=400, safe=False)

    if recognized_connection:
        filename = os.path.basename(recognized_connection)
        try:
            connection = Connection.objects.get(image__endswith=filename)
            connection_id = connection.id
            return JsonResponse({"result": connection_id}, status=200, safe=False)

        except Connection.DoesNotExist:
            return JsonResponse({"error": "Connection not found for the given image name."}, status=400, safe=False)

    else:
        return JsonResponse({"message": "doesn't exist", "image": body.get("image"), "rep": rep}, status=201, safe=False)
