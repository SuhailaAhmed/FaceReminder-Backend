from drf_yasg2 import openapi
from drf_yasg2.utils import swagger_auto_schema
from accounts.views.profile_views import profiles

profiles_endpoint = swagger_auto_schema(
    method='patch',
    manual_parameters=[  
        openapi.Parameter(
            name='fullname',
            in_=openapi.IN_FORM,
            type=openapi.TYPE_STRING,
            description='Full Name of user',
            required=False
        ),
        openapi.Parameter(
            name='phone',
            in_=openapi.IN_FORM,
            type=openapi.TYPE_STRING,
            description='Phone number of user',
            required=False
        ),
        openapi.Parameter(
            name='address',
            in_=openapi.IN_FORM,
            type=openapi.TYPE_STRING,
            description='Address of user',
            required=False
        ),
        openapi.Parameter(
            name='image',
            in_=openapi.IN_FORM,
            type=openapi.TYPE_FILE,
            description='Image of user',
            required=False
        ),
    ],
    responses={200: openapi.Response(
        "Profile updated sucessfully")}
)(profiles)