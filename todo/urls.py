from django.urls import path
from .views import (
    TaskList, TaskCreate, TaskUpdate, TaskDelete,
    CustomLoginView, RegisterPage, update_task_status, update_profile,
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('', TaskList.as_view(), name='tasks'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name='task-delete'),
    path('profile/', update_profile, name='profile'),
    path('api/update-task-status/', update_task_status, name='task-update-status'),
]
