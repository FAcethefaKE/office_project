
from office.models import TaskAssignmentConfirm


def unread_tasks(request):
    if request.user.is_authenticated:
        confirmation = TaskAssignmentConfirm.objects.filter(employee=request.user, is_read=False)
        unread_tasks_count = confirmation.count()
        has_unread_tasks = unread_tasks_count > 0
    else:
        unread_tasks_count = 0
        has_unread_tasks = False

    context = {
        'has_unread_tasks': has_unread_tasks,
        'unread_tasks_count': unread_tasks_count,
    }

    return context
