from django.urls import path
from . import views
from .views import TaskListAPIView

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tasks/', views.tasks, name='tasks'),
    path('calendar/', views.calendar, name='calendar'),
    path('members/', views.members, name='members'),
    path('task/<uuid:task_id>/', views.task_detail, name='task_detail'),
    path('task/create/', views.task_create, name='task_create'),
    path('task/<uuid:task_id>/edit/', views.task_edit, name='task_edit'),
    path('task/<uuid:task_id>/delete/', views.task_delete, name='task_delete'),
    path('task/<uuid:task_id>/delete/confirm/', views.confirm_delete_view, name='confirm_delete'),
    path('api/tasks/', views.api_tasks, name='api_tasks'),
    path('search/', views.search_tasks, name='task_search'),
    path('api/tasks/', TaskListAPIView.as_view(), name='task-list-api'),
    path('update-task-status/', views.update_task_status, name='update_task_status'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
