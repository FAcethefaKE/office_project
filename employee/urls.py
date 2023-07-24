from django.urls import path
from django.contrib.auth.views import LogoutView

from office_project import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('employee_login/', views.employee_login, name='employee_login'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('employee_home/', views.employee_home, name='employee_home'),
    path('employee_info/', views.employee_info, name='employee_info'),
    path('employee_task/', views.assigned_tasks, name='employee_task'),
    path('employee_task/mark_task_as_read/<int:task_id>/', views.mark_task_as_read, name='mark_task_as_read'),
    path('change_password/', views.change_password, name='password_change'),
    path('change_success/', views.change_password_success, name='password_change_success'),
]

urlpatterns += staticfiles_urlpatterns()
