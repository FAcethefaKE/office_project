from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from .models import EmployeeProfile, Task, TaskAssignmentConfirm


class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'time_card_nr', 'mobile', 'dob', 'nationality', 'address')


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'assign_date', 'assigned_employees_read_status')
    filter_horizontal = ('assigned_to',)

    def assigned_employees_read_status(self, obj):
        employees = obj.assigned_to.all()
        read_status = {employee: 'Read' if TaskAssignmentConfirm.objects.filter(task=obj, employee=employee,
                                                                                is_read=True).exists() else 'Not Read'
                       for employee in employees}
        return ', '.join([f'{employee} ({status})' for employee, status in read_status.items()])

    assigned_employees_read_status.short_description = 'Assigned Employees Read Status'


admin.site.register(CustomUser, UserAdmin)
admin.site.register(EmployeeProfile, EmployeeProfileAdmin)
admin.site.register(Task, TaskAdmin)
