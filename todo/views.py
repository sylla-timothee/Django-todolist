import json
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Task, Profile
from .forms import ProfileUpdateForm


class CustomLoginView(LoginView):
    template_name = 'todo/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'todo/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'todo/task_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_tasks = Task.objects.filter(user=self.request.user)
        context['todos'] = user_tasks.filter(status='todo')
        context['in_progress'] = user_tasks.filter(status='in_progress')
        context['dones'] = user_tasks.filter(status='done')
        return context


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title']
    success_url = reverse_lazy('tasks')
    template_name = 'todo/task_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = 'todo'
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title']
    success_url = reverse_lazy('tasks')
    template_name = 'todo/task_form.html'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    template_name = 'todo/task_confirm_delete.html'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


@require_POST
@login_required
def update_task_status(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    task_id = data.get('id')
    new_status = data.get('status')

    if not task_id or not new_status:
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    valid_statuses = [choice[0] for choice in Task.Status.choices]
    if new_status not in valid_statuses:
        return JsonResponse({'error': 'Invalid status'}, status=400)

    try:
        task = Task.objects.get(id=task_id, user=request.user)
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)

    task.status = new_status
    task.save()

    return JsonResponse({'success': True})


@login_required
def update_profile(request):
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('tasks')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'todo/profile.html', {'form': form})
