from django.db import models, IntegrityError
from django.utils.text import slugify


class User(models.Model):
    name = models.CharField(max_length=64)
    username = models.CharField(
        max_length=32, unique=True, help_text="Used in profile URL"
    )
    headline = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    @classmethod
    def create_for_name(cls, name):
        # Creates a new user for this name, with a unique username
        suffix = None
        while True:
            username = slugify(name)
            if suffix is not None:
                username = "{}-{}".format(username, suffix)
                suffix += 1
            else:
                suffix = 1
            try:
                return cls.objects.create(username=username, name=name)
            except IntegrityError:
                continue


class GoogleAccount(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="google_accounts",
        null=True,
        blank=True,
    )
    google_id = models.CharField(max_length=64, unique=True)
    email = models.EmailField()
    email_is_verified = models.BooleanField()
    name = models.CharField(max_length=128, null=True, blank=True)
    picture_url = models.CharField(max_length=255, null=True, blank=True)
    locale = models.CharField(max_length=8, null=True, blank=True)

    def __str__(self):
        return self.email
