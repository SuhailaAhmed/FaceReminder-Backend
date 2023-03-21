from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from accounts.models.connection import Connection
from accounts.serializers.connection import ConnectionSerializer


@api_view(
    [
        "POST",
    ]
)
@permission_classes([IsAuthenticated])
def create_connection(request):
    try:
        account = request.user

        image = request.data.get("image", None)

        if not image:
            return JsonResponse({"error": "missing `image` field"}, status=400)

        connection_serialized = ConnectionSerializer(data=request.data)

        if not connection_serialized.is_valid():
            return JsonResponse(connection_serialized.errors, status=400)

        connection_serialized.save(account=account)

        return JsonResponse(connection_serialized.data, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
