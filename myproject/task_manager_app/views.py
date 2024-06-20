from email import message
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.paginator import Paginator


from django.contrib.auth.decorators import login_required

from task_manager_app.forms import TaskForm
from task_manager_app.models import TaskList

def login(TemplateView):
    template_name = 'login.html'
    

"""Page views"""
def index(request):
    context = {
        'index_text':"Welcome Index Page.",
        }
    return render(request, 'index.html', context)

def contact(request):
    context = {
        'contact_text' : 'Welcome to the contact page',
    }
    return render(request, 'contact.html', context)

def about(request):
    context = {
        'about_text' : 'Welcome to the about page',
    }
    return render(request, 'about.html', context)

"""Todo views"""
#CREATE AND READ
@login_required
def todolist(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.manage = request.user
            instance.save()
        messages.success(request, ('New Task Added!'))
        return redirect('todolist')
    else:
        all_tasks = TaskList.objects.filter(manage=request.user)
        paginator = Paginator(all_tasks, 10)
        page = request.GET.get('pg')
        all_tasks = paginator.get_page(page)
        
        return render(request, 'todolist.html', {'all_tasks' : all_tasks})
    
#UPDATE
@login_required
def edit_task(request, task_id):
    if request.method == "PUT":
        task = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.PUT or None, instance=task)
        if form.is_valid():
            form.save()
        
        messages.success(request, ('Task Edited!'))
        return redirect('todolist')
    else:
        task_obj = TaskList.objects.get(pk=task_id)
        return render(request, 'edit.html', {'task_obj':task_obj})

#DELETE
@login_required
def delete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.delete()
    else:
        message.error(request, ('Access Denied, you are not allowed to delete this task.'))
        return redirect('todolist')

"""Complete and pending tasks"""
@login_required
def complete_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.done = True
        task.save()
    else:
       messages.error(request,("Access Restricted, You Are Not Allowed.")) 

    return redirect('todolist')

@login_required
def pending_task(request, task_id):
    task = TaskList.objects.get(pk=task_id)
    task.done = False
    task.save()

    return redirect('todolist')