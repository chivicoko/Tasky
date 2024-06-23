from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Task
from .forms import TaskForm
import random

@login_required
def index(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/index.html', {'tasks': tasks})

@login_required
def dashboard(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/dashboard.html', {'tasks': tasks})

@login_required
def tasks(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/tasks.html', {'tasks': tasks})

@login_required
def calendar(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/calendar.html', {'tasks': tasks})

@login_required
def members(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/members.html', {'tasks': tasks})

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'tasks/task_detail.html', {'task': task})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})
    
@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('/')  # Redirect to task list or any other appropriate view
    return redirect('confirm_delete', task_id=task_id)  # Redirect to confirmation view if not POST


@login_required
def confirm_delete_view(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})
    
@require_http_methods(["GET"])
def api_tasks(request):
    status = request.GET.get('status')
    if status:
        tasks = Task.objects.filter(status=status)
    else:
        tasks = Task.objects.all()
    data = list(tasks.values())
    return JsonResponse(data, safe=False)
