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
from django.core.exceptions import ValidationError


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Registration successful. Welcome!')
                return redirect('/')
            except ValidationError as e:
                form.add_error(None, e)
            except Exception as e:
                form.add_error(None, 'An unexpected error occurred during registration. Please try again.')
                messages.error(request, 'An unexpected error occurred during registration. Please try again.')
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
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'tasks/login.html', {'form': form})

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        # messages.success(request, 'You have been logged out successfully.')
    else:
        messages.info(request, 'You are not logged in.')
    return redirect('/')

@login_required
def index(request):
    tasks = Task.objects.all()
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        
        sort_by_priority = request.POST.get('sort_tasks')
        filter_by_priority = request.POST.get('filter_tasks')
        
        if filter_by_priority:
            tasks = Task.objects.filter(priority=filter_by_priority)
        elif sort_by_priority:
            tasks = Task.objects.order_by(sort_by_priority)
    
    return render(request, 'tasks/index.html', {'tasks': tasks, 'form': form})

@login_required
def dashboard(request):
    return render(request, 'tasks/dashboard.html', {'tasks': tasks})

@login_required
def tasks(request):
    return render(request, 'tasks/tasks.html', {'tasks': tasks})

@login_required
def calendar(request):
    return render(request, 'tasks/calendar.html', {'tasks': tasks})

@login_required
def members(request):
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
            task = form.save(commit=False)
            task.assigned_to = request.user
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('/')
        else:
            messages.error(request, 'There was an error creating the task. Please check the form for errors.')
    else:
        form = TaskForm()
    
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if task.assigned_to != request.user:
        messages.error(request, 'You do not have permission to edit this task.')
        return redirect('index')

    if request.method == 'POST':
        edit_form = TaskForm(request.POST, instance=task)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('/')
        else:
            messages.error(request, 'There was an error updating the task. Please check the form for errors.')
    else:
        edit_form = TaskForm(instance=task)
    
    return render(request, 'tasks/task_edit_form.html', {'form': edit_form, 'task': task})

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if task.assigned_to != request.user:
        messages.error(request, 'You do not have permission to delete this task.')
        return redirect('index')

    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('index')
    
    return render(request, 'tasks/confirm_delete.html', {'task': task})

@login_required
def confirm_delete_view(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if task.assigned_to != request.user:
        messages.error(request, 'You do not have permission to delete this task.')
        return redirect('index')
    
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
    filterset_fields = ['priority', 'due_date', 'category']
    ordering_fields = ['priority', 'due_date', 'category']

    def get_queryset(self):
        queryset = Task.objects.all()
        return queryset
    

@csrf_exempt
def update_task_status(request):
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
