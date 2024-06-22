from django.contrib import admin

from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'priority', 'due_date', 'category', 'assigned_to')
    search_fields = ('title', 'status', 'priority', 'due_date', 'category', 'assigned_to')
    list_filter = ('title', 'status', 'priority', 'due_date', 'category', 'assigned_to')


admin.site.register(Task, TaskAdmin)