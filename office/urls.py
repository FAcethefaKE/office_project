from django.urls import path
from django.contrib.auth.views import LogoutView

from office_project import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# from office_project.settings import DEBUG, STATIC_URL, MEDIA_URL, MEDIA_ROOT, STATIC_ROOT
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('admin_login/', views.admin_login, name="admin_login"),
    path('logout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),
    path('admin_home/', views.admin_home, name="admin_home"),
    path('view_all_emp/', views.view_all_emp, name="view_all_emp"),
    path('emp_add/', views.add_emp, name='emp_add'),
    path('add_success/', views.emp_add_success, name='emp_add_success'),
    path('employee_login/', views.employee_login, name="employee_login"),

]

urlpatterns += staticfiles_urlpatterns()
