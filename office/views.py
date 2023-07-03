# from django.contrib.auth.models import User
# from django.http import HttpResponse
# from django.shortcuts import get_object_or_404, redirect, render
# from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.decorators import login_required
# from django.core.paginator import Paginator
# from django.contrib import messages
#
# from django.contrib.auth import get_user_model
# from .forms import EmployeeRegistrationForm, EmployeeUpdateForm
# from .models import EmployeeProfile
#
#
# def index(request):
#     return render(request, 'index.html')
#
#
# def admin_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#
#         if user is not None and user.groups.filter(name='OfficeAdmin').exists():
#             login(request, user)
#             return redirect('admin_home')
#         else:
#             return render(request, 'admin_login.html', {'error': 'Invalid credentials or access denied.'})
#     else:
#         return render(request, 'admin_login.html')
#
#
# def admin_home(request):
#     return render(request, 'admin_home.html')
#
#
# # def employee_login(request):
# #     if request.method == 'POST':
# #         try:
# #             user = User.objects.get(Email=request.POST['Email'], Password=request.POST['Password'])
# #             return redirect('home')
# #         except User.DoesNotExist:
# #             return render(request, 'employee_login.html', {'error': 'Username or password is incorrect!'})
# #     else:
# #         return render(request, 'employee_login.html')
#
#
# def employee_login(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         user = authenticate(request, username=email, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('employee_home')
#         else:
#             return render(request, 'employee_login.html', {'error': 'Username or password is incorrect!'})
#     else:
#         return render(request, 'employee_login.html')
#
#
# def employee_home(request):
#     return render(request, 'employee_home.html')
#
#
# @login_required(login_url='/admin_login')
# def view_all_emp(request):
#     if request.user.is_authenticated:
#         # employees = EmployeeProfile.objects.all().order_by('id')
#         users_to_exclude = User.objects.filter(username__in=['admin', 'zivile'])
#         employees = EmployeeProfile.objects.exclude(user__in=users_to_exclude).order_by('id')
#
#     paginator = Paginator(employees, 5)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     context = {
#         'employee': page_obj,
#         'employee_number': (page_obj.number - 1) * paginator.per_page,
#         'data': 'Employees list',
#     }
#     if not employees:
#         context['error'] = 'There is no Employee Info'
#     return render(request, 'view_all_emp.html',  context)
#
#
# @login_required(login_url='/admin_login')
# def add_emp(request):
#     data = 'Register new Employee'
#     if request.method == 'POST':
#         form = EmployeeRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('emp_add_success')
#     else:
#         form = EmployeeRegistrationForm()
#     return render(request, 'employee_add.html', {'form': form, 'data': data})
#
#
# def emp_add_success(request):
#     form = EmployeeRegistrationForm()
#     return render(request, 'emp_add_success.html', {'form': form})
#
#
# @login_required(login_url='/admin_login')
# def employee_update(request, emp_id):
#     employee = get_object_or_404(EmployeeProfile, id=emp_id)
#     user = employee.user
#     data = f'Update employee: {user.first_name } { user.last_name}'
#
#     if request.method == 'POST':
#         form = EmployeeUpdateForm(request.POST, instance=employee)
#         if form.is_valid():
#             form.save()
#             return redirect('emp_update_success')
#     else:
#         initial_data = {
#             'first_name': user.first_name,
#             'last_name': user.last_name,
#             'email': user.email,
#         }
#         form = EmployeeUpdateForm(instance=employee, initial=initial_data)
#
#     return render(request, 'employee_update.html', {'form': form, 'employee': employee, 'data': data})
#
#
# def emp_update_success(request):
#     form = EmployeeUpdateForm()
#     return render(request, 'emp_update_success.html', {'form': form})
#
#
# @login_required(login_url='/admin_login')
# def employee_delete(request, emp_id):
#     employee = get_object_or_404(EmployeeProfile, id=emp_id)
#     data = 'Delete Employee from DB'
#     # user = employee.user
#     if request.method == 'POST':
#         employee.delete()
#         return redirect('view_all_emp')
#
#     return render(request, 'employee_delete.html', {'employee': employee, 'data': data})
