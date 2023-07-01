from django.contrib import admin
# from .models import Employee
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from .models import EmployeeProfile


class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'time_card_nr', 'mobile', 'dob', 'nationality', 'address')


admin.site.register(EmployeeProfile, EmployeeProfileAdmin)












# class AdminAdmin(admin.ModelAdmin):
#     list_display = ('id', 'username')
#     search_fields = ('username',)


# class EmployeeAdmin(admin.ModelAdmin):
#     list_display = ('time_card_nr', 'full_name', 'dob', 'mobile', 'nationality', 'address')
#     search_fields = ('username',)


# admin.site.register(Admin, AdminAdmin)
# admin.site.register(Employee, EmployeeAdmin)