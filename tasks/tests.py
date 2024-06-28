from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task
from .forms import TaskForm
import uuid

class TaskTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            status='In_progress',
            priority='High',
            due_date='2023-12-31',
            category='Work',
            assigned_to=self.user
        )

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/index.html')
        self.assertContains(response, 'Test Task')

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/dashboard.html')
        self.assertContains(response, 'Test Task')

    def test_task_detail_view(self):
        response = self.client.get(reverse('task_detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_detail.html')
        self.assertContains(response, 'Test Task')

    def test_task_create_view(self):
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')
        self.assertIsInstance(response.context['form'], TaskForm)

        response = self.client.post(reverse('task_create'), {
            'title': 'New Task',
            'description': 'New Description',
            'status': 'Completed',
            'priority': 'Medium',
            'due_date': '2023-12-31',
            'category': 'Personal',
            'assigned_to': self.user.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_task_edit_view(self):
        response = self.client.get(reverse('task_edit', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_edit_form.html')
        self.assertIsInstance(response.context['form'], TaskForm)

        response = self.client.post(reverse('task_edit', args=[self.task.id]), {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'status': 'Completed',
            'priority': 'Medium',
            'due_date': '2023-12-31',
            'category': 'Work',
            'assigned_to': self.user.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')

    def test_task_delete_view(self):
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=self.task.id)

    def test_login_view(self):
        self.client.logout()
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_register_view(self):
        self.client.logout()
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_search_tasks(self):
        response = self.client.get(reverse('task_search'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/search_results.html')
        self.assertContains(response, 'Test Task')

    def test_api_tasks(self):
        response = self.client.get(reverse('api_tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['title'], 'Test Task')

    def test_update_task_status(self):
        response = self.client.post(
            reverse('update_task_status'),
            data=json.dumps({'taskId': str(self.task.id), 'newStatus': 'Completed'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, 'Completed')
