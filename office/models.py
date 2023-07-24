from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


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


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    assign_date = models.DateTimeField(blank=False)
    assigned_to = models.ManyToManyField(CustomUser, related_name='assigned_tasks')

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        """Create TaskAssignmentConfirm instances for users"""
        if created:
            for user in self.assigned_to.all():
                TaskAssignmentConfirm.objects.get_or_create(task=self, employee=user)

    def __str__(self):
        return self.title


class TaskAssignmentConfirm(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    read_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Task Assignment Confirmation: Task-{self.task.id}, " \
               f"Employee-{self.employee.first_name}{self.employee.last_name}, Read-{self.is_read}"
