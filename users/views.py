from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseRedirect
from django.utils.text import slugify
from .models import User, GoogleAccount
from .utils import set_cookie_for_user, clear_cookie_for_user
import requests


def homepage(request):
    return render(request, "homepage.html", {"auth": request.auth})


def signin(request):
    return render(
        request,
        "signin.html",
        {"google_client_id": settings.GOOGLE_CLIENT_ID, "auth": request.auth},
    )


def signout(request):
    response = HttpResponseRedirect("/")
    clear_cookie_for_user(response)
    return response


@csrf_exempt
def signin_for_cookie(request):
    "Ajax endpoint for exchanging id_token for a cookie"
    id_token = request.POST.get("id_token") or ""
    if not id_token:
        return JsonResponse({"ok": False, "error": "id_token is required"})
    # Urgh this is so ugly
    # https://developers.google.com/identity/sign-in/web/backend-auth#calling-the-tokeninfo-endpoint
    data = requests.get(
        "https://oauth2.googleapis.com/tokeninfo", params={"id_token": id_token}
    ).json()
    if "error" in data:
        return JsonResponse({"ok": False, "error": data["message"]})
    # It worked! Create an account or sign them in
    google_account, created = GoogleAccount.objects.get_or_create(
        google_id=data["sub"],
        defaults={
            "email": data["email"],
            "email_is_verified": data["email_verified"] == "true",
            "name": data["name"],
            "picture_url": data["picture"],
            "locale": data["locale"],
        },
    )
    user = None
    if google_account.user is None:
        # We need to create them a user! First figure out a username
        user = User.create_for_name(data["name"])
        google_account.user = user
        google_account.save()
    else:
        user = google_account.user
    # Set cookie for that user
    response = JsonResponse(
        {
            "ok": True,
            "user": {"id": user.pk, "name": user.name, "username": user.username},
        }
    )
    set_cookie_for_user(response, google_account.user)
    return response
