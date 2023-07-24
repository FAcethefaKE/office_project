from django.contrib.auth.forms import PasswordChangeForm

from office.models import CustomUser


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = CustomUser
