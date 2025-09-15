from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm
from .models import Task ,TaskComment

def index(request):
    my_lists = [("/secure/task/list/","Task: мои объекты"), ("/secure/taskcomment/list/","TaskComment: мои объекты")]
    return render(request, "index.html", {"my_lists": my_lists, "domain_desc": "Задачи и комментарии"})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user:
                login(request, user); messages.success(request, "OK"); return redirect("index")
            messages.error(request, "Неверные данные")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request); messages.info(request, "Вышли")
    return redirect("index")

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

@login_required
def task_list(request):
    objs = Task.objects.filter(owner=request.user).order_by("-id")
    return render(request, "tasksapp/task_list.html", {"objects": objs})

def task_detail_vuln(request):
    obj_id = request.GET.get("id")
    obj = get_object_or_404(Task, id=obj_id)
    return render(request, "tasksapp/task_detail.html", {"obj": obj, "mode": "vuln_query"})

@login_required
def task_detail_secure(request, obj_id):
    obj = get_object_or_404(Task, id=obj_id, owner=request.user)
    return render(request, "tasksapp/task_detail.html", {"obj": obj, "mode": "secure"})

def task_detail_vuln_path(request, obj_id):
    obj = get_object_or_404(Task, id=obj_id)
    return render(request, "tasksapp/task_detail.html", {"obj": obj, "mode": "vuln_path"})

@require_POST
def task_update_vuln(request, obj_id):
    obj = get_object_or_404(Task, id=obj_id)
    if 'title' in request.POST:
        setattr(obj, 'title', request.POST['title'])
    obj.save()
    return redirect("index")


from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

@login_required
def taskcomment_list(request):
    objs = TaskComment.objects.filter(owner=request.user).order_by("-id")
    return render(request, "tasksapp/taskcomment_list.html", {"objects": objs})

def taskcomment_detail_vuln(request):
    obj_id = request.GET.get("id")
    obj = get_object_or_404(TaskComment, id=obj_id)
    return render(request, "tasksapp/taskcomment_detail.html", {"obj": obj, "mode": "vuln_query"})

@login_required
def taskcomment_detail_secure(request, obj_id):
    obj = get_object_or_404(TaskComment, id=obj_id, owner=request.user)
    return render(request, "tasksapp/taskcomment_detail.html", {"obj": obj, "mode": "secure"})

def taskcomment_detail_vuln_path(request, obj_id):
    obj = get_object_or_404(TaskComment, id=obj_id)
    return render(request, "tasksapp/taskcomment_detail.html", {"obj": obj, "mode": "vuln_path"})

@require_POST
def taskcomment_update_vuln(request, obj_id):
    obj = get_object_or_404(TaskComment, id=obj_id)
    if 'text' in request.POST:
        setattr(obj, 'text', request.POST['text'])
    obj.save()
    return redirect("index")
