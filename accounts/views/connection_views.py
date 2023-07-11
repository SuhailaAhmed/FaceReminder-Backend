from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from accounts.facenet_final_class import add_new_representation
from accounts.models.connection import Connection, get_image_folder_path
from accounts.serializers.connection import ConnectionSerializer
from Gp_Backend import settings


def create_connection(request):
    # try:
    account = request.user

    image = request.data.get("image", None)
    rep = request.data.get("rep", None)

    if not image:
        return JsonResponse({"error": "missing `image` field"}, status=400)

    if not rep:
        return JsonResponse({"error": "missing `rep` field"}, status=400)

    connection_serialized = ConnectionSerializer(data=request.data)

    if not connection_serialized.is_valid():
        return JsonResponse(connection_serialized.errors, status=400)

    connection_serialized.save(account=account)

    account_id = account.id
    folder_path = f"{settings.FOLDER1_PATH}/{account_id}"
    image_url = connection_serialized.data.get("image")
    image_path = f"{settings.BASE_DIR}{image_url}"
    add_new_representation(image_path, rep, folder_path)

    return JsonResponse(connection_serialized.data, status=201)
    # except Exception as e:
    #     return JsonResponse({"error": str(e)}, status=400)


def update_connection(request, connection_id):
    try:
        account = request.user
        connection = account.connections.get(id=connection_id)
        connection_serialized = ConnectionSerializer(instance=connection, data=request.data, partial=True)
        if connection_serialized.is_valid():
            connection_serialized.save()
            return JsonResponse(connection_serialized.data, status=200)
        else:
            return JsonResponse(connection_serialized.errors, status=400)
    except Connection.DoesNotExist:
        return JsonResponse({"error": "There's no connection with this id for this account!"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def retrieve_connections(request):
    account = request.user
    connections = account.connections.all()
    connections_serializer = ConnectionSerializer(instance=connections, many=True)
    return JsonResponse(connections_serializer.data, status=200, safe=False)


def retrieve_single_connection(request, connection_id):
    try:
        account = request.user
        connection = account.connections.get(id=connection_id)
        connection_serializer = ConnectionSerializer(instance=connection)
        return JsonResponse(connection_serializer.data, status=200)
    except Connection.DoesNotExist:
        return JsonResponse({"error": "There's no connection with this id for this account!"}, status=400)


@api_view(["POST", "GET"])
@permission_classes(
    [
        IsAuthenticated,
    ]
)
def connections(request):
    if request.method == "POST":
        return create_connection(request)
    elif request.method == "GET":
        return retrieve_connections(request)


@api_view(["PATCH", "GET"])
@permission_classes(
    [
        IsAuthenticated,
    ]
)
def connection(request, connection_id):
    if request.method == "PATCH":
        return update_connection(request, connection_id)
    elif request.method == "GET":
        return retrieve_single_connection(request, connection_id)
