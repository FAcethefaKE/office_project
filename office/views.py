from django.utils import timezone
from django.db import transaction

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator

from .forms import EmployeeRegistrationForm, EmployeeUpdateForm, TaskCreateForm
from .models import CustomUser, TaskAssignmentConfirm, EmployeeProfile, Task


def index(request):
    return render(request, 'index.html')


def is_admin(user):
    return user.is_authenticated and user.is_superuser


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.groups.filter(name='OfficeAdmin').exists():
            login(request, user)
            return redirect('admin_home')
        else:
            return render(request, 'admin_login.html', {'error': 'Invalid credentials or access denied.'})
    else:
        return render(request, 'admin_login.html')


@user_passes_test(is_admin, login_url='/admin_login')
def admin_home(request):
    return render(request, 'admin_home.html')


@login_required(login_url='/admin_login')
@user_passes_test(is_admin, login_url='/admin_login')
def view_all_emp(request):
    if request.user.is_authenticated:
        users_to_exclude = CustomUser.objects.filter(username__in=['admin', 'zivile'])
        employees = EmployeeProfile.objects.exclude(user__in=users_to_exclude).order_by('id')

    paginator = Paginator(employees, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'employee': page_obj,
        'employee_number': (page_obj.number - 1) * paginator.per_page,
        'data': 'Employees list',
    }
    if not employees:
        context['error'] = 'There is no Employee Info'
    return render(request, 'view_all_emp.html',  context)


@login_required(login_url='/admin_login')
@user_passes_test(is_admin, login_url='/admin_login')
def add_emp(request):
    data = 'Register new Employee'
    if request.method == 'POST':
        form = EmployeeRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('emp_add_success')
    else:
        form = EmployeeRegistrationForm()
    return render(request, 'employee_add.html', {'form': form, 'data': data})


def emp_add_success(request):
    form = EmployeeRegistrationForm()
    return render(request, 'emp_add_success.html', {'form': form})


@login_required(login_url='/admin_login')
@user_passes_test(is_admin, login_url='/admin_login')
def employee_update(request, emp_id):
    employee = get_object_or_404(EmployeeProfile, id=emp_id)
    user = employee.user
    data = f'Update employee: {user.first_name } { user.last_name}'

    if request.method == 'POST':
        form = EmployeeUpdateForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('emp_update_success')
    else:
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
        form = EmployeeUpdateForm(instance=employee, initial=initial_data)

    context = {'form': form, 'employee': employee, 'data': data}
    return render(request, 'employee_update.html', context)


def emp_update_success(request):
    form = EmployeeUpdateForm()
    return render(request, 'emp_update_success.html', {'form': form})


@login_required(login_url='/admin_login')
@user_passes_test(is_admin, login_url='/admin_login')
def employee_delete(request, emp_id):
    employee = get_object_or_404(EmployeeProfile, id=emp_id)
    data = 'Delete Employee from DB'
    if request.method == 'POST':
        employee.delete()
        return redirect('view_all_emp')

    context = {'employee': employee, 'data': data}
    return render(request, 'employee_delete.html', context)


@login_required(login_url='/admin_login')
@user_passes_test(is_admin, login_url='/admin_login')
def task_add(request):
    data = 'Create Task Assignment'
    if request.method == 'POST':
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_all_task')
    else:
        form = TaskCreateForm()

    context = {'form': form, 'data': data}
    return render(request, 'task_add.html', context)


@login_required(login_url='/admin_login')
@user_passes_test(is_admin, login_url='/admin_login')
def view_all_task(request):
    tasks = Task.objects.all().order_by('assign_date')
    show_outdated = request.GET.get('show_outdated', 'false') == 'true'

    if not show_outdated:
        tasks = tasks.filter(assign_date__gte=timezone.now().date())

    confirmation_office = TaskAssignmentConfirm.objects.all()

    paginator = Paginator(tasks, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'task': page_obj,
        'task_number': (page_obj.number - 1) * paginator.per_page,
        'data': 'Assigned tasks',
        'show_outdated': show_outdated,
        'confirmation_office': confirmation_office,
    }

    if not tasks:
        context['error'] = 'There are no Tasks assigned'

    return render(request, 'view_all_task.html',  context)


@login_required(login_url='/admin_login')
@user_passes_test(is_admin, login_url='/admin_login')
def task_update(request, tsk_id):
    task = get_object_or_404(Task, id=tsk_id)
    data = 'Update Task: {}'.format(task.title)

    if request.method == 'POST':
        form = TaskCreateForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            """Retrieve the updated assigned users after saving the form"""
            new_assigned_users = set(task.assigned_to.all())

            """Add or remove TaskAssignmentConfirm instances based on changes in assigned users"""
            with transaction.atomic():
                TaskAssignmentConfirm.objects.filter(task=task, employee__in=new_assigned_users).update(is_read=False)

                for user in new_assigned_users:
                    """Get or create TaskAssignmentConfirm for each user and task"""
                    TaskAssignmentConfirm.objects.get_or_create(task=task, employee=user, defaults={'is_read': False})
                """Update is_read for existing TaskAssignmentConfirm instances"""
                TaskAssignmentConfirm.objects.filter(task=task).exclude(employee__in=new_assigned_users).delete()

            return redirect('task_update_success')
    else:
        """Highlight the assigned employees"""
        assigned_employees = task.assigned_to.all()
        form = TaskCreateForm(instance=task, initial={'employees': assigned_employees})

    context = {'form': form, 'data': data}

    return render(request, 'task_update.html', context)


def task_update_success(request):
    form = TaskCreateForm()
    return render(request, 'task_update_success.html', {'form': form})


@login_required(login_url='/admin_login')
@user_passes_test(is_admin, login_url='/admin_login')
def task_delete(request, tsk_id):
    task = get_object_or_404(Task, id=tsk_id)
    data = 'Delete Task from DB'

    if request.method == 'POST':
        task.delete()
        return redirect('view_all_task')

    context = {'task': task, 'data': data}
    return render(request, 'task_delete.html', context)


def go_back(request):
    previous_url = request.META.get('HTTP_REFERER', '/')
    return redirect(previous_url)
