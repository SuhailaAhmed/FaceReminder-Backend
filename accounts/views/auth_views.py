from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from accounts.serializers import AccountSerializer 
from accounts.models.account import Account
from accounts.models.tokens import AccountToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.core import mail
from Gp_Backend import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.timezone import make_aware
from datetime import datetime, timedelta

# Create your views here.

@api_view(['Post',])
def register(request):
    body = request.data

    if body['password'] != body['confirm_password']:
        return JsonResponse({'messgae' : 'two passwords are not identical'}, status=400)

    if len(body['password']) < 8:
        return JsonResponse({'message': 'password must be at least 8 characters'}, status=400)

    if not body['password'].isalnum():
        return JsonResponse({'message': 'password must be alphanumeric'}, status=400)

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
@permission_classes([IsAuthenticated,])
def logout(request):
    try:
        user = request.user
        token = Token.objects.get(user=user)
        token.delete()
        return JsonResponse({'message': 'logout sucessfully'}, status=200)

    except Token.DoesNotExist:

        return JsonResponse({'error': 'no token for this user'}, status=400)

@api_view(['Post',])
def forget_password(request):
    email = request.data.get('email', None)
    
    if not email:
        return JsonResponse({'error': 'email must be sent in body'}, status=400)

    try:
        account = Account.objects.get(email=email)
        token = AccountToken.objects.get(account=account)
        token.delete()
        token = AccountToken.objects.create(account=account)
    except AccountToken.DoesNotExist:
        token = AccountToken.objects.create(account=account)
    except Account.DoesNotExist:
        return JsonResponse({'error': 'No Account with this email'}, status=400)


    subject = "GP Account password reset"
    link = settings.FORGET_PASSWORD_URL + str(token.uuid)
    message = render_to_string(
        'accounts/forget_password.html', {'link': link, 'fullname': account.fullname})
    plain_message = strip_tags(message)
    mail.send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [email], html_message=message)
    return JsonResponse({'message': 'Reset Password link is sent successfully'}, status=200)

@api_view(['Get',])
def check_token(request, token):
    try:
        token = AccountToken.objects.get(uuid=token)
        time_now = make_aware(datetime.now())
        if token.created_at + timedelta(days=1) < time_now:
            token.delete()
            return JsonResponse({'error': 'Token is expired'}, status=400)
        token.created_at = time_now
        token.save()
        return JsonResponse({'message': 'Token is valid'}, status=200)
    except AccountToken.DoesNotExist:
        return JsonResponse({'error': 'No Token with this uuid'}, status=400)
    
@api_view(['Post',])
def set_password(request, token):
    try:
        
        token = AccountToken.objects.get(uuid=token)
        time_now = make_aware(datetime.now())
        if token.created_at + timedelta(days=1) < time_now:
            token.delete()
            return JsonResponse({'error': 'Token is expired'}, status=400)

        password = request.data.get('password', None)
        confirm_password = request.data.get('confirm_password', None)
        if not password:
            return JsonResponse({'error': 'password must be sent in body'}, status=400)
        
        if not confirm_password:
            return JsonResponse({'error': 'confirm_password must be sent in body'}, status=400)
        
        if password != confirm_password:
            return JsonResponse({'messgae' : 'two passwords are not identical'}, status=400)

        if len(password) < 8:
            return JsonResponse({'message': 'password must be at least 8 characters'}, status=400)

        if not (password.isalnum() and not password.isalpha() and not password.isdigit()):
            return JsonResponse({'message': 'password must be alphanumeric'}, status=400)
                
        account = token.account
        account.set_password(password)
        account.save()
        token.delete()
        return JsonResponse({'message': 'Password is changed successfully'}, status=200)

    except AccountToken.DoesNotExist:
        return JsonResponse({'error': 'No Token with this uuid'}, status=400)