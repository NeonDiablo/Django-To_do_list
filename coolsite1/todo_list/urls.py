from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home_task, name='home_task'),
    path('tasks', views.all_tasks, name='all_task'),
    path('task/<int:pk>/', views.single_task, name='single_task'),
    path('task-create/', views.create_task, name='create_task'),
    path('task-update/<int:pk>/', views.update_task, name='update_task'),
    path('task-delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('login/', views.login_task, name='login_task'),
    path('logout/', views.logout_task, name='logout_task'),
    path('registration/', views.user_registration, name='user_registration'),
    path('activate/<uidb>/<token>/', views.email_activation, name='activate'),
    path('tasks/searched', views.searched, name='searched'),
    
]

urlpatterns += [
    path('captcha/', include('captcha.urls')),
]
