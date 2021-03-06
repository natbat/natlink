# Generated by Django 2.1.7 on 2019-03-30 20:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="GoogleAccount",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("google_id", models.CharField(max_length=64, unique=True)),
                ("email", models.EmailField(max_length=254)),
                ("email_is_verified", models.BooleanField()),
                ("name", models.CharField(blank=True, max_length=128, null=True)),
                (
                    "picture_url",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("locale", models.CharField(blank=True, max_length=8, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64)),
                (
                    "username",
                    models.CharField(
                        help_text="Used in profile URL", max_length=32, unique=True
                    ),
                ),
                ("headline", models.CharField(blank=True, max_length=255, null=True)),
                ("bio", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name="googleaccount",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="google_accounts",
                to="users.User",
            ),
        ),
    ]
