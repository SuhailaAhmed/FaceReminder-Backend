from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from accounts.serializers.profile import ProfileSerializer


def get_profile(request):
    try:
        account = request.user
        print(account)
        profile = account.profile
        profile_serialized = ProfileSerializer(profile)
        return JsonResponse(profile_serialized.data, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def update_profile(request):
    return


@api_view(["Get", "Patch"])
@permission_classes([IsAuthenticated])
def profiles(request):
    if request.method == "GET":
        return get_profile(request)
    elif request.method == "PATCH":
        return update_profile(request)
