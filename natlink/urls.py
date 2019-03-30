from django.contrib import admin
from django.urls import path
from users.views import signin, signin_for_cookie, signout, homepage

urlpatterns = [
    path("", homepage),
    path("signin/", signin),
    path("signin/exchange-for-cookie/", signin_for_cookie),
    path("signout/", signout),
    path("admin/", admin.site.urls),
]
