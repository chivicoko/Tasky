from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date', 'category', 'assigned_to']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'border border-gray-400 rounded p-2 w-full text-gray-600',
                'placeholder': 'Enter task title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'border border-gray-400 rounded p-2 w-full text-gray-600',
                'rows': 4,
                'placeholder': 'Enter task description'
            }),
            'status': forms.Select(attrs={
                'class': 'border border-gray-400 rounded p-2 w-full text-gray-600',
            }),
            'priority': forms.Select(attrs={
                'class': 'border border-gray-400 rounded p-2 w-full text-gray-600',
            }),
            'due_date': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'border border-gray-400 rounded p-2 w-full text-gray-600',
                'placeholder': 'YYYY-MM-DD'
            }),
            'category': forms.TextInput(attrs={
                'class': 'border border-gray-400 rounded p-2 w-full text-gray-600',
                'placeholder': 'Enter task category'
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'border border-gray-400 rounded p-2 w-full text-gray-600',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['due_date'].input_formats = ['%Y-%m-%d', '%d/%m/%Y']
