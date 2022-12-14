from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from accounts.serializers import AccountSerializer 
from accounts.models import Account
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

# Create your views here.

@api_view(['Post',])
def register(request):
    body = request.data

    if body['password'] != body['confirm_password']:
        return JsonResponse({'messgae' : 'two passwords are not identical'}, status=400)

    account_serialized = AccountSerializer(data=body)

    if not account_serialized.is_valid():
        return JsonResponse(account_serialized.errors, status=400)
        
    account = account_serialized.save()
    account.set_password(body['password'])
    account.save()
    token, created = Token.objects.get_or_create(user=account)

    return JsonResponse({'fullname': account.fullname, "token": token.key}, status= 201)


@api_view(['Post',])
def login(request):
    body = request.data
    email = body.get('email',None)
    password = body.get('password',None)

    if not email:
        return JsonResponse({'error': 'email must be sent in body'}, status=400)

    if not password:
        return JsonResponse({'error': 'password must be sent in body'}, status=400)

    try:
        account = Account.objects.get(email= email)

        if not account.check_password(password):
            return JsonResponse({'error': 'Wrong password'}, status=400)

        token, created = Token.objects.get_or_create(user=account)
        return JsonResponse({'token': token.key, 'fullname': account.fullname}, status=200)

    except Account.DoesNotExist:
        return JsonResponse({'error': 'No Account with this email'}, status=400)

    
@api_view(['Get',])
# @permission_classes([IsAuthenticated])
def logout(request):

    try:
        user = request.user
        print(user)
        print(Token.objects.all())
        token = Token.objects.get(user=user)
        token.delete()
        return JsonResponse({'message': 'logout sucessfully'}, status=200)

    except Token.DoesNotExist:
        return JsonResponse({'error': 'no token for this user'}, status=400)