from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from accounts.serializers.profile import ProfileSerializer


@api_view(['GET',])
@permission_classes([IsAuthenticated,])
def get_profile(request):
    try:
        account = request.user
        profile = account.profile
        profile_serialized = ProfileSerializer(profile)
        return JsonResponse(profile_serialized.data, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)