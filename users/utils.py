from .models import User

COOKIE_NAME = "natlink_auth"
COOKIE_SALT = "natlink-auth"


def set_cookie_for_user(response, user):
    response.set_signed_cookie(
        COOKIE_NAME,
        user.pk,
        salt=COOKIE_SALT,
        max_age=365 * 24 * 60 * 60,
        httponly=True,
        samesite="Strict",
    )


def clear_cookie_for_user(response):
    response.delete_cookie(COOKIE_NAME)


def user_auth_middleware(get_response):
    def middleware(request):
        user_id = request.get_signed_cookie(COOKIE_NAME, default=None, salt=COOKIE_SALT)
        if user_id:
            request.auth = User.objects.get(pk=user_id)
        else:
            request.auth = None
        return get_response(request)

    return middleware
