from django.db import models


class User(models.Model):
    name = models.CharField(max_length=64)
    username = models.CharField(
        max_length=32, unique=True, help_text="Used in profile URL"
    )
    headline = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class GoogleAccount(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="google_accounts"
    )
    google_id = models.CharField(max_length=64, unique=True)
    email = models.EmailField()
    email_is_verified = models.BooleanField()
    name = models.CharField(max_length=128, null=True, blank=True)
    picture_url = models.CharField(max_length=255, null=True, blank=True)
    locale = models.CharField(max_length=8, null=True, blank=True)

    def __str__(self):
        return self.email
