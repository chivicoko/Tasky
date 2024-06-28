from django import forms
from .models import Task

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date', 'category', 'assigned_to']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'border border-gray-400 rounded p-2 w-full text-gray-600',
                'placeholder': 'Enter task title',
                'id': 'modal-task-form-title-input',
            }),
            'description': forms.Textarea(attrs={
                'class': 'border border-gray-400 rounded p-2 w-full text-gray-600',
                'rows': 4,
                'placeholder': 'Enter task description',
                'id': 'modal-task-form-description-input',
            }),
            'status': forms.Select(attrs={
                'class': 'border border-gray-400 rounded p-2 w-full text-gray-600',
                'id': 'modal-task-form-status-input',
            }),
            'priority': forms.Select(attrs={
                'class': 'border border-gray-400 rounded p-2 w-full text-gray-600',
                'id': 'modal-task-form-priority-input',
            }),
            'due_date': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'border border-gray-400 rounded p-2 w-full text-gray-600',
                'placeholder': 'YYYY-MM-DD',
                'id': 'modal-task-form-duedate-input',
            }),
            'category': forms.TextInput(attrs={
                'class': 'border border-gray-400 rounded p-2 w-full text-gray-600',
                'placeholder': 'Enter task category',
                'id': 'modal-task-form-category-input',
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'border border-gray-400 rounded p-2 w-full text-gray-600',
                'id': 'modal-task-form-assigned-to-input',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['due_date'].input_formats = ['%Y-%m-%d', '%d/%m/%Y']


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600 text-gray-600',
                'placeholder': 'Enter your email'
            }),
        )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600 text-gray-600',
            'placeholder': 'Enter your username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600 text-gray-600',
            'placeholder': 'Enter your password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600 text-gray-600',
            'placeholder': 'Confirm your password'
        })


    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600 text-gray-600',
        'placeholder': 'Enter your username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600 text-gray-600',
        'placeholder': 'Enter your password'
    }))

