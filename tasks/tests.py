from django.test import TestCase
from django.contrib.auth.models import User
from .models import Task

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            status='in_progress',
            priority='medium',
            due_date='2024-06-21 12:00',
            category='test',
            assigned_to=self.user
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.status, 'in_progress')

class TaskViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            status='in_progress',
            priority='medium',
            due_date='2024-06-21 12:00',
            category='test',
            assigned_to=self.user
        )

    def test_index_view(self):
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')
