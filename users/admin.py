from django.contrib import admin
from .models import User, GoogleAccount

admin.site.register(User)
admin.site.register(GoogleAccount)
