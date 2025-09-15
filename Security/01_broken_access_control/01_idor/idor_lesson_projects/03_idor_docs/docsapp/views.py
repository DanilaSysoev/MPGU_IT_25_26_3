from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm
from .models import Document ,FileEntry

def index(request):
    my_lists = [("/secure/document/list/","Document: мои объекты"), ("/secure/fileentry/list/","FileEntry: мои объекты")]
    return render(request, "index.html", {"my_lists": my_lists, "domain_desc": "Документы и файлы"})

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
def document_list(request):
    objs = Document.objects.filter(owner=request.user).order_by("-id")
    return render(request, "docsapp/document_list.html", {"objects": objs})

def document_detail_vuln(request):
    obj_id = request.GET.get("id")
    obj = get_object_or_404(Document, id=obj_id)
    return render(request, "docsapp/document_detail.html", {"obj": obj, "mode": "vuln_query"})

@login_required
def document_detail_secure(request, obj_id):
    obj = get_object_or_404(Document, id=obj_id, owner=request.user)
    return render(request, "docsapp/document_detail.html", {"obj": obj, "mode": "secure"})

def document_detail_vuln_path(request, obj_id):
    obj = get_object_or_404(Document, id=obj_id)
    return render(request, "docsapp/document_detail.html", {"obj": obj, "mode": "vuln_path"})

@require_POST
def document_update_vuln(request, obj_id):
    obj = get_object_or_404(Document, id=obj_id)
    if 'title' in request.POST:
        setattr(obj, 'title', request.POST['title'])
    obj.save()
    return redirect("index")


from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

@login_required
def fileentry_list(request):
    objs = FileEntry.objects.filter(owner=request.user).order_by("-id")
    return render(request, "docsapp/fileentry_list.html", {"objects": objs})

def fileentry_detail_vuln(request):
    obj_id = request.GET.get("id")
    obj = get_object_or_404(FileEntry, id=obj_id)
    return render(request, "docsapp/fileentry_detail.html", {"obj": obj, "mode": "vuln_query"})

@login_required
def fileentry_detail_secure(request, obj_id):
    obj = get_object_or_404(FileEntry, id=obj_id, owner=request.user)
    return render(request, "docsapp/fileentry_detail.html", {"obj": obj, "mode": "secure"})

def fileentry_detail_vuln_path(request, obj_id):
    obj = get_object_or_404(FileEntry, id=obj_id)
    return render(request, "docsapp/fileentry_detail.html", {"obj": obj, "mode": "vuln_path"})

@require_POST
def fileentry_update_vuln(request, obj_id):
    obj = get_object_or_404(FileEntry, id=obj_id)
    if 'name' in request.POST:
        setattr(obj, 'name', request.POST['name'])
    obj.save()
    return redirect("index")
