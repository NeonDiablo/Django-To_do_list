from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import RegisterForm, TaskForm, LoginForm
from django.contrib import messages as msg
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site  
    

from django.contrib.auth.models import User  
from django.conf import settings
from django.template.loader import render_to_string  

from django.core.mail import EmailMessage 
from django.utils.encoding import force_bytes 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.http import HttpResponseNotFound
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import Http404


def home_task(request):
    return render(request, 'todo_list/main_page.html')


@login_required
def all_tasks(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'todo_list/all_tasks.html', {'tasks':tasks})

@login_required
def single_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.user == request.user:
        return render(request, 'todo_list/single_task.html', {'task':task})
    raise Http404

@login_required
def create_task(request):
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()   
            return redirect('all_task')
        else:
            msg.error(request, 'Incorrect data')
    else:
        return render(request, 'todo_list/create_task.html', {'form':form})


@login_required
def update_task(request, pk):
    instance = get_object_or_404(Task, pk=pk)
    if instance.user == request.user:
        if request.method == 'POST':
            form = TaskForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                return redirect('all_task')
            else:
                msg.error(request, 'Incorrect data')

        form = TaskForm(instance=instance)
        return render(request, 'todo_list/update_task.html', {'form':form})
            
    else:
        return HttpResponseNotFound('Not found')

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if task.user == request.user:
        task.delete()
        return redirect('all_task')
    return HttpResponseNotFound('Not found')
    



def login_task(request):
    form = LoginForm
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username = data['username'], password = data['password'])
            if user is not None:
                login(request, user)
                return redirect('all_task')
            else:
                msg.error(request, 'Login or password incorrect')
        else:
            msg.error(request, 'Invalid form')

    return render(request,'todo_list/login_task.html', {'form':form})



@login_required
def logout_task(request):
    logout(request)
    return redirect('login_task')


def user_registration(request):
    if not (settings.EMAIL_HOST_USER or settings.EMAIL_HOST_PASSWORD):
        raise Http404('Update settings.py, EMAIL')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            if not User.objects.get(email=user_email):
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                
                token = token_generator.make_token(user)
                uidb = urlsafe_base64_encode(force_bytes(user.pk)) 
                current_site = get_current_site(request)
                email_context = {'user':user,
                                 'token':token,
                                 'uidb':uidb,
                                 'domen':current_site.domain,
                                }
                template = render_to_string('todo_list/activation.html', context=email_context)
                #As long as there is no mail data in settings, will not be a valid form
                email = EmailMessage(
                'TO-DO-LIST', #title
                    template, #body 
                        settings.EMAIL_HOST_USER, #server email
                            [user_email], #user email
                )
            
                email.send(fail_silently=False)
                msg.success(request, f'Check your Email - {user.email}')
                return redirect('home_task')
            else:
                msg.error(request, 'This Email is already taken')
        else:
            msg.error(request, 'Incorrect form')
                        
    form = RegisterForm()
    return render(request, 'todo_list/register.html', {'form':form,})



def email_activation(request, uidb, token):
    try:
        user_pk = urlsafe_base64_decode(uidb)
        user = User.objects.get(pk=user_pk)
        if user and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('login_task')
        
    except (User.DoesNotExist, ValueError,
            TypeError, OverflowError, ValidationError) as email_exception:
        user = None
        print(email_exception)
        raise Http404


@login_required
def searched(request):
    context = {}
    if request.method == 'POST' and request.POST['searched'] != '':
        data = request.POST['searched']
        tasks = Task.objects.filter(user=request.user).filter(
                                     Q(title__icontains=data) | 
                                     Q(description__icontains=data)
                                     )
        context['searched'] = data
        context['tasks'] = tasks
    return render(request, 'todo_list/searched.html', context)