from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.models import User

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import datetime


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # def __str__(self):
    #     return self.username


class EmployeeProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
                                related_name='employee_profile')
    time_card_nr = models.CharField(max_length=5, unique=True)
    mobile = models.CharField(max_length=10, blank=True)
    dob = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class TaskManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(assign_date__gte=timezone.now().date())


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    assign_date = models.DateTimeField(blank=False)
    assigned_to = models.ManyToManyField(CustomUser)

    def __str__(self):
        return self.title




# class EmployeeManager(UserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('username', email)
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         extra_fields.setdefault('email', email)
#
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#
#         user = self.model(**extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#
#         return user
#
#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#
#         return self.create_user(email, password, **extra_fields)
# #
#
# class Employee(AbstractUser):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
#                                 null=True, related_name='employee_profile')
#     time_card_nr = models.CharField(max_length=5, unique=True)
#     full_name = models.CharField(max_length=100)
#     mobile = models.CharField(max_length=10, blank=True)
#     dob = models.DateField(blank=True, null=True)
#     nationality = models.CharField(max_length=20, blank=True)
#     address = models.CharField(max_length=100, blank=True)
#     # email = models.EmailField(max_length=20, null=False, unique=True)
#     groups = models.ManyToManyField(Group, blank=True, related_name='employee_profiles')
#     user_permissions = models.ManyToManyField(Permission, blank=True, related_name='employee_profiles')
#     REQUIRED_FIELDS = ['email']
#     USERNAME_FIELD = 'username'
#
#     objects = EmployeeManager()
#

# class CustomLogEntry(models.Model):
#     log_entry = models.OneToOneField(LogEntry, on_delete=models.CASCADE, primary_key=True)
#     employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
#
#     # Additional fields as per your requirements
#
#     class Meta:
#         verbose_name_plural = 'Custom Log Entries'



# class CustomLogEntry(models.Model):
#     log_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='log_entries')
#     # Add any additional fields or customization you need
#
#     class Meta:
#         app_label = 'office'
#         db_table = 'custom_log_entry'
#
# try:
#     admin.site.register(CustomLogEntry)
# except AlreadyRegistered:
#     pass

# class Employee(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
#     # time_card_nr = models.CharField(max_length=5, unique=True)
#     # mobile = models.CharField(max_length=10)
#     # address = models.CharField(max_length=255)
#     groups = models.ManyToManyField(Group, blank=True, related_name='employee_profiles')
#     user_permissions = models.ManyToManyField(Permission, blank=True, related_name='employee_profiles')
