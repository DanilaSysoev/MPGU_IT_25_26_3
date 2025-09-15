from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm
from .models import Grade ,Assignment

def index(request):
    my_lists = [("/secure/grade/list/","Grade: мои объекты"), ("/secure/assignment/list/","Assignment: мои объекты")]
    return render(request, "index.html", {"my_lists": my_lists, "domain_desc": "Оценки и задания"})

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
def grade_list(request):
    objs = Grade.objects.filter(owner=request.user).order_by("-id")
    return render(request, "gradesapp/grade_list.html", {"objects": objs})

def grade_detail_vuln(request):
    obj_id = request.GET.get("id")
    obj = get_object_or_404(Grade, id=obj_id)
    return render(request, "gradesapp/grade_detail.html", {"obj": obj, "mode": "vuln_query"})

@login_required
def grade_detail_secure(request, obj_id):
    obj = get_object_or_404(Grade, id=obj_id, owner=request.user)
    return render(request, "gradesapp/grade_detail.html", {"obj": obj, "mode": "secure"})

def grade_detail_vuln_path(request, obj_id):
    obj = get_object_or_404(Grade, id=obj_id)
    return render(request, "gradesapp/grade_detail.html", {"obj": obj, "mode": "vuln_path"})

@require_POST
def grade_update_vuln(request, obj_id):
    obj = get_object_or_404(Grade, id=obj_id)
    if 'title' in request.POST:
        setattr(obj, 'title', request.POST['title'])
    obj.save()
    return redirect("index")


from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

@login_required
def assignment_list(request):
    objs = Assignment.objects.filter(owner=request.user).order_by("-id")
    return render(request, "gradesapp/assignment_list.html", {"objects": objs})

def assignment_detail_vuln(request):
    obj_id = request.GET.get("id")
    obj = get_object_or_404(Assignment, id=obj_id)
    return render(request, "gradesapp/assignment_detail.html", {"obj": obj, "mode": "vuln_query"})

@login_required
def assignment_detail_secure(request, obj_id):
    obj = get_object_or_404(Assignment, id=obj_id, owner=request.user)
    return render(request, "gradesapp/assignment_detail.html", {"obj": obj, "mode": "secure"})

def assignment_detail_vuln_path(request, obj_id):
    obj = get_object_or_404(Assignment, id=obj_id)
    return render(request, "gradesapp/assignment_detail.html", {"obj": obj, "mode": "vuln_path"})

@require_POST
def assignment_update_vuln(request, obj_id):
    obj = get_object_or_404(Assignment, id=obj_id)
    if 'title' in request.POST:
        setattr(obj, 'title', request.POST['title'])
    obj.save()
    return redirect("index")
