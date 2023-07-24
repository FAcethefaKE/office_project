from django.utils import timezone

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from office.forms import EmployeeRegistrationForm
from office.models import Task, TaskAssignmentConfirm

from .forms import CustomPasswordChangeForm


def employee_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('employee_home')
        else:
            return render(request, 'employee_login.html', {'error': 'Username or password is incorrect!'})
    else:
        return render(request, 'employee_login.html')


@login_required(login_url='/employee_login')
def employee_home(request):
    return render(request, 'employee_home.html')


@login_required(login_url='/employee_login')
def employee_info(request):
    employee_profile = request.user.employee_profile
    user = employee_profile.user
    form = EmployeeRegistrationForm(instance=employee_profile, initial={
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    })
    form.fields.pop('password')

    for field_name in form.fields:
        form.fields[field_name].widget.attrs['readonly'] = True

    data = 'Your personal data'
    context = {'form': form, 'data': data}
    return render(request, 'employee_info.html', context)


@login_required(login_url='/employee_login')
def assigned_tasks(request):
    employee = request.user.employee_profile
    tasks = Task.objects.filter(assigned_to=employee.user).order_by('assign_date')
    show_outdated = request.GET.get('show_outdated', 'false') == 'true'

    if not show_outdated:
        tasks = tasks.filter(assign_date__gte=timezone.now().date())

    confirmation = TaskAssignmentConfirm.objects.filter(task__in=tasks, employee=request.user)

    paginator = Paginator(tasks, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'task': page_obj,
        'task_number': (page_obj.number - 1) * paginator.per_page,
        'data': 'Assigned tasks',
        'show_outdated': show_outdated,
        'confirmation': confirmation,
    }

    if not tasks:
        context['error'] = 'There are no Tasks assigned'

    return render(request, 'employee_task.html', context)


@login_required(login_url='/employee_login')
def mark_task_as_read(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    employee = request.user.employee_profile

    if request.method == 'POST':
        is_read = request.POST.get('is_read', False)
        task_confirmations = TaskAssignmentConfirm.objects.get(task=task, employee=employee.user)

        if is_read == 'True' and not task_confirmations.is_read:
            task_confirmations.is_read = True
            task_confirmations.read_date = timezone.now()
            task_confirmations.save()

        return redirect('employee_task')

    return redirect('employee_task')


@login_required(login_url='/employee_login')
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('password_change_success')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'password_change.html', {'form': form})


def change_password_success(request):
    return render(request, 'password_change_success.html')
