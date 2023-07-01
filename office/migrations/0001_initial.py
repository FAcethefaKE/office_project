# Generated by Django 4.1.1 on 2023-06-28 20:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="EmployeeProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("time_card_nr", models.CharField(max_length=5, unique=True)),
                ("full_name", models.CharField(max_length=100)),
                ("mobile", models.CharField(blank=True, max_length=10)),
                ("dob", models.DateField(blank=True, null=True)),
                ("nationality", models.CharField(blank=True, max_length=20)),
                ("address", models.CharField(blank=True, max_length=100)),
                (
                    "user",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="employee_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]