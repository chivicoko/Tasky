from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm, RegisterForm, CustomAuthenticationForm
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from .models import Task
from .serializers import TaskSerializer
from django.views.decorators.csrf import csrf_exempt
import json


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'tasks/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'tasks/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

# @login_required
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
            return redirect('index')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

# @login_required
# def task_edit(request, task_id):
#     task = get_object_or_404(Task, pk=task_id)
#     if request.method == 'POST':
#         form = TaskForm(request.POST, instance=task)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#     else:
#         form = TaskForm(instance=task)
#     return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def edit_or_create_task(request, task_id=None):
    if task_id:
        task = get_object_or_404(Task, pk=task_id)
        form = TaskForm(request.POST or None, instance=task)
        is_editing = True
    else:
        form = TaskForm(request.POST or None)
        is_editing = False

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('index')

    context = {
        'form': form,
        'is_editing': is_editing,
    }
    return render(request, 'tasks/task_form.html', context)
    
@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('index')
    return redirect('confirm_delete', task_id=task_id)

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

@login_required
def search_tasks(request):
    query = request.GET.get('q')
    tasks = Task.objects.filter(title__icontains=query) | Task.objects.filter(description__icontains=query)

    in_progress_count = tasks.filter(status='In_progress').count()
    completed_count = tasks.filter(status='Completed').count()
    overdue_count = tasks.filter(status='Overdue').count()
    
    context = {
        'tasks': tasks,
        'query': query,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
        'overdue_count': overdue_count
    }
    
    return render(request, 'tasks/search_results.html', context)


class TaskListAPIView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['priority', 'due_date', 'category']  # Define fields for filtering
    ordering_fields = ['priority', 'due_date', 'category']  # Define fields for ordering

    def get_queryset(self):
        queryset = Task.objects.all()
        return queryset
    

# update task status
@csrf_exempt
def update_task_status(request):
    # if request.user.is_authenticated:
    if request.method == 'POST':
        data = json.loads(request.body)
        task_id = data.get('taskId')
        new_status = data.get('newStatus')

        try:
            task = Task.objects.get(id=task_id)
            task.status = new_status
            task.save()
            return JsonResponse({"success": True}, status=200)
        except Task.DoesNotExist:
            return JsonResponse({"success": False, "error": "Task not found"}, status=404)
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)
