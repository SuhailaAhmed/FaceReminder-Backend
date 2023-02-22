from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser
from django.http import JsonResponse
from accounts.serializers.connection import ConnectionSerializer
from accounts.models.connection import Connection


@api_view(
    [
        "Post",
    ]
)
@permission_classes([IsAuthenticated])
def create_connection(request):
    try:
        account = request.user

        name = request.data.get("name", None)
        relation = request.data.get("relation", None)

        if not name:
            return JsonResponse({"error": "missing `name` field"}, status=400)

        if not relation:
            return JsonResponse({"error": "missing `relation` field"}, status=400)

        connection_serialized = ConnectionSerializer(data=request.data, partial=True)

        if not connection_serialized.is_valid():
            return JsonResponse(connection_serialized.errors, status=400)

        connection_serialized.save(account=account)

        return JsonResponse(connection_serialized.data, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
