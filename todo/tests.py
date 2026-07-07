import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Task, Profile


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_task_creation_default_status(self):
        task = Task.objects.create(user=self.user, title='Test task')
        self.assertEqual(task.status, 'todo')

    def test_task_status_choices_exist(self):
        choices = dict(Task.Status.choices)
        self.assertIn('todo', choices)
        self.assertIn('in_progress', choices)
        self.assertIn('done', choices)

    def test_task_str_method(self):
        task = Task.objects.create(user=self.user, title='Test task')
        self.assertEqual(str(task), 'Test task')

    def test_task_belongs_to_user(self):
        task = Task.objects.create(user=self.user, title='Test task')
        self.assertEqual(task.user, self.user)


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_profile_created_with_user(self):
        self.assertTrue(Profile.objects.filter(user=self.user).exists())

    def test_profile_str_method(self):
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(str(profile), f'Profil de {self.user.username}')

    def test_profile_default_avatar(self):
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.avatar.name, 'default.png')


class AuthViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/login.html')

    def test_login_redirect_if_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('tasks'))

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/register.html')

    def test_register_creates_user(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        self.assertRedirects(response, reverse('tasks'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_redirect_if_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('register'))
        self.assertRedirects(response, reverse('tasks'))


class TaskListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.other_user = User.objects.create_user(username='otheruser', password='testpass123')

        self.task1 = Task.objects.create(user=self.user, title='Todo task', status='todo')
        self.task2 = Task.objects.create(user=self.user, title='In progress task', status='in_progress')
        self.task3 = Task.objects.create(user=self.user, title='Done task', status='done')
        self.other_task = Task.objects.create(user=self.other_user, title='Other task', status='todo')

    def test_task_list_requires_login(self):
        response = self.client.get(reverse('tasks'))
        self.assertRedirects(response, f'{reverse("login")}?next={reverse("tasks")}')

    def test_task_list_shows_only_user_tasks(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/task_list.html')
        self.assertContains(response, 'Todo task')
        self.assertContains(response, 'In progress task')
        self.assertContains(response, 'Done task')
        self.assertNotContains(response, 'Other task')

    def test_task_list_context_has_three_lists(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('tasks'))
        self.assertIn('todos', response.context)
        self.assertIn('in_progress', response.context)
        self.assertIn('dones', response.context)

    def test_task_list_context_counts(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('tasks'))
        self.assertEqual(len(response.context['todos']), 1)
        self.assertEqual(len(response.context['in_progress']), 1)
        self.assertEqual(len(response.context['dones']), 1)

    def test_new_user_has_empty_lists(self):
        new_user = User.objects.create_user(username='newuser2', password='testpass123')
        self.client.login(username='newuser2', password='testpass123')
        response = self.client.get(reverse('tasks'))
        self.assertEqual(len(response.context['todos']), 0)
        self.assertEqual(len(response.context['in_progress']), 0)
        self.assertEqual(len(response.context['dones']), 0)


class TaskCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_task_create_requires_login(self):
        response = self.client.get(reverse('task-create'))
        self.assertRedirects(response, f'{reverse("login")}?next={reverse("task-create")}')

    def test_task_create_sets_user(self):
        self.client.login(username='testuser', password='testpass123')
        self.client.post(reverse('task-create'), {'title': 'New task'})
        task = Task.objects.get(title='New task')
        self.assertEqual(task.user, self.user)

    def test_task_create_default_status(self):
        self.client.login(username='testuser', password='testpass123')
        self.client.post(reverse('task-create'), {'title': 'New task'})
        task = Task.objects.get(title='New task')
        self.assertEqual(task.status, 'todo')

    def test_task_create_uses_correct_template(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('task-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/task_form.html')


class TaskUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.other_user = User.objects.create_user(username='otheruser', password='testpass123')
        self.task = Task.objects.create(user=self.user, title='Original title', status='todo')

    def test_task_update_requires_login(self):
        response = self.client.get(reverse('task-update', args=[self.task.id]))
        self.assertRedirects(response, f'{reverse("login")}?next={reverse("task-update", args=[self.task.id])}')

    def test_task_update_modifies_task(self):
        self.client.login(username='testuser', password='testpass123')
        self.client.post(reverse('task-update', args=[self.task.id]), {'title': 'Updated title'})
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated title')

    def test_user_cannot_update_others_task(self):
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.get(reverse('task-update', args=[self.task.id]))
        self.assertEqual(response.status_code, 404)

    def test_task_update_uses_correct_template(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('task-update', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/task_form.html')

    def test_task_update_redirects_to_tasks(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('task-update', args=[self.task.id]), {'title': 'Updated'})
        self.assertRedirects(response, reverse('tasks'))


class TaskDeleteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.other_user = User.objects.create_user(username='otheruser', password='testpass123')
        self.task = Task.objects.create(user=self.user, title='Task to delete', status='todo')

    def test_task_delete_requires_login(self):
        response = self.client.get(reverse('task-delete', args=[self.task.id]))
        self.assertRedirects(response, f'{reverse("login")}?next={reverse("task-delete", args=[self.task.id])}')

    def test_task_delete_removes_task(self):
        self.client.login(username='testuser', password='testpass123')
        self.client.post(reverse('task-delete', args=[self.task.id]))
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_task_delete_confirm_template(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('task-delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/task_confirm_delete.html')

    def test_user_cannot_delete_others_task(self):
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.post(reverse('task-delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 404)


class UpdateTaskStatusViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.other_user = User.objects.create_user(username='otheruser', password='testpass123')
        self.task = Task.objects.create(user=self.user, title='Test task', status='todo')
        self.url = reverse('task-update-status')

    def test_update_status_requires_login(self):
        response = self.client.post(self.url, json.dumps({'id': self.task.id, 'status': 'in_progress'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 302)

    def test_update_status_valid_move_to_in_progress(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.url, json.dumps({'id': self.task.id, 'status': 'in_progress'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, 'in_progress')

    def test_update_status_valid_move_to_done(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.url, json.dumps({'id': self.task.id, 'status': 'done'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, 'done')

    def test_update_status_valid_move_back_to_todo(self):
        self.task.status = 'in_progress'
        self.task.save()
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.url, json.dumps({'id': self.task.id, 'status': 'todo'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, 'todo')

    def test_update_status_invalid_status(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.url, json.dumps({'id': self.task.id, 'status': 'invalid'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update_status_nonexistent_task(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.url, json.dumps({'id': 9999, 'status': 'done'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_update_status_other_users_task(self):
        self.client.login(username='otheruser', password='testpass123')
        response = self.client.post(self.url, json.dumps({'id': self.task.id, 'status': 'done'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_update_status_missing_id(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.url, json.dumps({'status': 'done'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update_status_missing_status(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.url, json.dumps({'id': self.task.id}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update_status_wrong_method(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_update_status_invalid_json(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.url, 'not json', content_type='application/json')
        self.assertEqual(response.status_code, 400)


class TaskListTemplateAccessibilityTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        Task.objects.create(user=self.user, title='Test task', status='todo')
        self.client.login(username='testuser', password='testpass123')
        self.response = self.client.get(reverse('tasks'))

    def test_task_list_has_three_columns(self):
        self.assertContains(self.response, 'data-status="todo"')
        self.assertContains(self.response, 'data-status="in_progress"')
        self.assertContains(self.response, 'data-status="done"')

    def test_columns_have_aria_label(self):
        self.assertContains(self.response, 'aria-label="Colonne À faire"')
        self.assertContains(self.response, 'aria-label="Colonne En cours"')
        self.assertContains(self.response, 'aria-label="Colonne Terminé"')

    def test_task_lists_have_aria_label(self):
        self.assertContains(self.response, 'aria-label="Tâches à faire"')
        self.assertContains(self.response, 'aria-label="Tâches en cours"')
        self.assertContains(self.response, 'aria-label="Tâches terminées"')

    def test_live_region_exists(self):
        self.assertContains(self.response, 'aria-live="polite"')

    def test_cards_have_data_id(self):
        self.assertContains(self.response, 'data-id')


class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_profile_view_requires_login(self):
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, f'{reverse("login")}?next={reverse("profile")}')

    def test_profile_view_uses_correct_template(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/profile.html')

    def test_profile_update(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('profile'), {})
        self.assertRedirects(response, reverse('tasks'))
