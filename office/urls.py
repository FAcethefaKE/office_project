from django.urls import path
from django.contrib.auth.views import LogoutView

from office_project import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('admin_home/', views.admin_home, name='admin_home'),

    path('emp_add/', views.add_emp, name='emp_add'),
    path('add_success/', views.emp_add_success, name='emp_add_success'),
    path('view_all_emp/', views.view_all_emp, name='view_all_emp'),
    path('view_all_emp/emp_update/<int:emp_id>/', views.employee_update, name='emp_update'),
    path('update_success/', views.emp_update_success, name='emp_update_success'),
    path('emp_delete/<int:emp_id>/', views.employee_delete, name='emp_delete'),

    path('task_add/', views.task_add, name='task_add'),
    path('view_all_task/', views.view_all_task, name='view_all_task'),
    path('view_all_task/update_task/<int:tsk_id>', views.task_update, name='task_update'),
    path('task_success/', views.task_update_success, name='task_update_success'),
    path('view_all_task/delete_task/<int:tsk_id>', views.task_delete, name='task_delete'),

]

urlpatterns += staticfiles_urlpatterns()
