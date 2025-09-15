from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm
from .models import Product ,Supply

def index(request):
    my_lists = [("/secure/product/list/","Product: мои объекты"), ("/secure/supply/list/","Supply: мои объекты")]
    return render(request, "index.html", {"my_lists": my_lists, "domain_desc": "Склад: товары и поставки"})

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
def product_list(request):
    objs = Product.objects.filter(owner=request.user).order_by("-id")
    return render(request, "invapp/product_list.html", {"objects": objs})

def product_detail_vuln(request):
    obj_id = request.GET.get("id")
    obj = get_object_or_404(Product, id=obj_id)
    return render(request, "invapp/product_detail.html", {"obj": obj, "mode": "vuln_query"})

@login_required
def product_detail_secure(request, obj_id):
    obj = get_object_or_404(Product, id=obj_id, owner=request.user)
    return render(request, "invapp/product_detail.html", {"obj": obj, "mode": "secure"})

def product_detail_vuln_path(request, obj_id):
    obj = get_object_or_404(Product, id=obj_id)
    return render(request, "invapp/product_detail.html", {"obj": obj, "mode": "vuln_path"})

@require_POST
def product_update_vuln(request, obj_id):
    obj = get_object_or_404(Product, id=obj_id)
    if 'name' in request.POST:
        setattr(obj, 'name', request.POST['name'])
    obj.save()
    return redirect("index")


from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

@login_required
def supply_list(request):
    objs = Supply.objects.filter(owner=request.user).order_by("-id")
    return render(request, "invapp/supply_list.html", {"objects": objs})

def supply_detail_vuln(request):
    obj_id = request.GET.get("id")
    obj = get_object_or_404(Supply, id=obj_id)
    return render(request, "invapp/supply_detail.html", {"obj": obj, "mode": "vuln_query"})

@login_required
def supply_detail_secure(request, obj_id):
    obj = get_object_or_404(Supply, id=obj_id, owner=request.user)
    return render(request, "invapp/supply_detail.html", {"obj": obj, "mode": "secure"})

def supply_detail_vuln_path(request, obj_id):
    obj = get_object_or_404(Supply, id=obj_id)
    return render(request, "invapp/supply_detail.html", {"obj": obj, "mode": "vuln_path"})

@require_POST
def supply_update_vuln(request, obj_id):
    obj = get_object_or_404(Supply, id=obj_id)
    if 'title' in request.POST:
        setattr(obj, 'title', request.POST['title'])
    obj.save()
    return redirect("index")
