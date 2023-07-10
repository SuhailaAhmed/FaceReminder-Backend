import os
import shutil
from datetime import datetime, timedelta

from django.core import mail
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.timezone import make_aware
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from accounts.models.account import Account
from accounts.models.profile import Profile
from accounts.models.token import AccountToken
from accounts.serializers.account import AccountSerializer
from Gp_Backend import settings

# Create your views here.


def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


def has_characters(inputString):
    return any(char.isalpha() for char in inputString)


@api_view(
    [
        "Post",
    ]
)
def register(request):
    body = request.data
    password = request.data.get("password", None)
    confirm_password = request.data.get("confirm_password", None)
    full_name = request.data.get("fullname", None)

    if not password:
        return JsonResponse({"error": "Please write password!"}, status=400)

    if not confirm_password:
        return JsonResponse({"error": "Please confirm your password!"}, status=400)

    if password != confirm_password:
        return JsonResponse({"messgae": "Password and Confirm passwords aren't the same!"}, status=400)

    if len(password) < 8:
        return JsonResponse({"message": "Password must be at least 8 characters!"}, status=400)

    if not has_numbers(password) or not has_characters(password):
        return JsonResponse({"message": "Password must contain numbers and characters!"}, status=400)

    if not full_name:
        return JsonResponse({"error": "Please write your full name!"}, status=400)

    account_serialized = AccountSerializer(data=body)

    if not account_serialized.is_valid():
        return JsonResponse(account_serialized.errors, status=400)

    account = account_serialized.save()
    account.set_password(password)
    account.save()

    token, created = Token.objects.get_or_create(user=account)

    Profile.objects.create(account=account, fullname=full_name)

    account_id = account.id
    destination_folder = f"{settings.FOLDER1_PATH}\{account_id}"

    source_path = os.path.join(settings.MEDIA_ROOT, "example.jpg")
    if not os.path.exists(source_path):
        return JsonResponse({"error": "Source image not found."}, status=404)

    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Copy the image file to the destination folder
    destination_path = os.path.join(destination_folder, "example.jpg")
    shutil.copy2(source_path, destination_path)

    return JsonResponse({"token": token.key, "account": AccountSerializer(account).data}, status=201)


@api_view(
    [
        "Post",
    ]
)
def login(request):
    body = request.data
    email = body.get("email", None)
    password = body.get("password", None)

    if not email:
        return JsonResponse({"error": "Please write your email!"}, status=400)

    if not password:
        return JsonResponse({"error": "Please write your password!"}, status=400)

    try:
        account = Account.objects.get(email=email)

        if not account.check_password(password):
            return JsonResponse({"error": "Wrong password!"}, status=400)

        token, created = Token.objects.get_or_create(user=account)
        return JsonResponse({"token": token.key, "account": AccountSerializer(account).data}, status=200)

    except Account.DoesNotExist:
        return JsonResponse({"error": "There's no Account with this email!"}, status=400)


@api_view(
    [
        "Get",
    ]
)
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        user = request.user
        token = Token.objects.get(user=user)
        token.delete()
        return JsonResponse({"message": "logout sucessfully."}, status=200)

    except Token.DoesNotExist:
        return JsonResponse({"error": "You are already loged out!"}, status=400)


@api_view(
    [
        "Post",
    ]
)
def forget_password(request):
    email = request.data.get("email", None)

    if not email:
        return JsonResponse({"error": "Please write your email!"}, status=400)

    try:
        account = Account.objects.get(email=email)
    except Account.DoesNotExist:
        return JsonResponse({"error": "There's no Account with this email!"}, status=400)

    try:
        token = AccountToken.objects.get(account=account)
        token.delete()
        token = AccountToken.objects.create(account=account)
    except AccountToken.DoesNotExist:
        token = AccountToken.objects.create(account=account)

    subject = "GP Account password reset"
    link = settings.FORGET_PASSWORD_URL + str(token.uuid)
    message = render_to_string("accounts/forget_password.html", {"link": link, "fullname": account.profile.fullname})
    plain_message = strip_tags(message)
    mail.send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [email], html_message=message)
    return JsonResponse({"message": "Reset Password link is sent successfully."}, status=200)


@api_view(
    [
        "Get",
    ]
)
def check_token(request, token):
    try:
        token = AccountToken.objects.get(uuid=token)
        time_now = make_aware(datetime.now())
        if token.created_at + timedelta(days=1) < time_now:
            token.delete()
            return JsonResponse({"error": "Token is expired."}, status=400)
        token.created_at = time_now
        token.save()
        return JsonResponse({"message": "Token is valid."}, status=200)
    except AccountToken.DoesNotExist:
        return JsonResponse({"error": "This token does not exist!"}, status=400)


@api_view(
    [
        "Post",
    ]
)
def set_password(request, token):
    try:
        token = AccountToken.objects.get(uuid=token)
        time_now = make_aware(datetime.now())
        if token.created_at + timedelta(days=1) < time_now:
            token.delete()
            return JsonResponse({"error": "Token is expired!"}, status=400)
        password = request.data.get("password", None)
        confirm_password = request.data.get("confirm_password", None)
        if not password:
            return JsonResponse({"error": "Please write password!"}, status=400)

        if not confirm_password:
            return JsonResponse({"error": "Please confirm your password!"}, status=400)

        if password != confirm_password:
            return JsonResponse({"messgae": "Password and Confirm passwords aren't the same!"}, status=400)

        if len(password) < 8:
            return JsonResponse({"message": "Password must be at least 8 characters!"}, status=400)

        if not (password.isalnum() and not password.isalpha() and not password.isdigit()):
            return JsonResponse({"message": "Password must contain numbers and characters!"}, status=400)

        account = token.account
        account.set_password(password)
        account.save()
        token.delete()
        return JsonResponse({"message": "Password is changed successfully"}, status=200)

    except AccountToken.DoesNotExist:
        return JsonResponse({"error": "Token does not exist!"}, status=400)
