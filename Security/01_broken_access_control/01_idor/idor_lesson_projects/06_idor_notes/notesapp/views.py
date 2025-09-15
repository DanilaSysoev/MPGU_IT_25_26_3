from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm
from .models import Note ,Category

def index(request):
    my_lists = [("/secure/note/list/","Note: мои объекты"), ("/secure/category/list/","Category: мои объекты")]
    return render(request, "index.html", {"my_lists": my_lists, "domain_desc": "Заметки и категории"})

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
def note_list(request):
    objs = Note.objects.filter(owner=request.user).order_by("-id")
    return render(request, "notesapp/note_list.html", {"objects": objs})

def note_detail_vuln(request):
    obj_id = request.GET.get("id")
    obj = get_object_or_404(Note, id=obj_id)
    return render(request, "notesapp/note_detail.html", {"obj": obj, "mode": "vuln_query"})

@login_required
def note_detail_secure(request, obj_id):
    obj = get_object_or_404(Note, id=obj_id, owner=request.user)
    return render(request, "notesapp/note_detail.html", {"obj": obj, "mode": "secure"})

def note_detail_vuln_path(request, obj_id):
    obj = get_object_or_404(Note, id=obj_id)
    return render(request, "notesapp/note_detail.html", {"obj": obj, "mode": "vuln_path"})

@require_POST
def note_update_vuln(request, obj_id):
    obj = get_object_or_404(Note, id=obj_id)
    if 'title' in request.POST:
        setattr(obj, 'title', request.POST['title'])
    obj.save()
    return redirect("index")


from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

@login_required
def category_list(request):
    objs = Category.objects.filter(owner=request.user).order_by("-id")
    return render(request, "notesapp/category_list.html", {"objects": objs})

def category_detail_vuln(request):
    obj_id = request.GET.get("id")
    obj = get_object_or_404(Category, id=obj_id)
    return render(request, "notesapp/category_detail.html", {"obj": obj, "mode": "vuln_query"})

@login_required
def category_detail_secure(request, obj_id):
    obj = get_object_or_404(Category, id=obj_id, owner=request.user)
    return render(request, "notesapp/category_detail.html", {"obj": obj, "mode": "secure"})

def category_detail_vuln_path(request, obj_id):
    obj = get_object_or_404(Category, id=obj_id)
    return render(request, "notesapp/category_detail.html", {"obj": obj, "mode": "vuln_path"})

@require_POST
def category_update_vuln(request, obj_id):
    obj = get_object_or_404(Category, id=obj_id)
    if 'name' in request.POST:
        setattr(obj, 'name', request.POST['name'])
    obj.save()
    return redirect("index")
