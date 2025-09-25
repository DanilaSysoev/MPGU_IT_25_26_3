from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from .forms import LoginForm
from .models import Profile, Item

def _get_profile(user):
    return Profile.objects.get_or_create(user=user)[0]

def index(request):
    my_lists = [("/secure/items/", "Мои объекты")]
    actions = [
        ("/vuln/delete_user/2/", "Удалить пользователя (уязвимо: без серверной проверки роли)"),
        ("/vuln/admin_panel/", "Админ-панель (только клиентская проверка)"),
        ("/vuln/promote_user/2/?role=admin", "Повышение роли (уязвимо: неверный RBAC — доверяет параметру role)"),
    ]
    return render(request, "index.html", {"my_lists": my_lists, "actions": actions, "domain_desc": "Блог: модерация комментариев, удаление пользователей и назначение ролей"})

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

@login_required
def items_list(request):
    items = Item.objects.filter(owner=request.user).order_by("-id")
    return render(request, "items_list.html", {"items": items})

@login_required
def delete_user_vuln(request, user_id):
    if request.user.is_staff:
        user = get_object_or_404(User, id=user_id)
        user.delete()
        messages.warning(request, f"Пользователь {user.username} удалён (уязвимо).")
        return redirect("index")
    return HttpResponseForbidden("Admin only")

@login_required
def delete_user_secure(request, user_id):
    prof = _get_profile(request.user)
    if prof.role != "admin":
        return HttpResponseForbidden("Admin only")
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, f"Удалено админом: {user.username}")
    return redirect("index")

@login_required
def admin_panel_vuln(request):
    if request.user.is_staff:        
        return render(request, "admin_panel.html", {"mode": "vuln"})
    else:
        return HttpResponseForbidden("Admin only")

@login_required
def admin_panel_secure(request):
    if _get_profile(request.user).role != "admin":
        return HttpResponseForbidden("Admin only")
    return render(request, "admin_panel.html", {"mode": "secure"})

@login_required
def promote_user_vuln(request, user_id):
    if request.user.is_staff:
        target = get_object_or_404(User, id=user_id)
        role = request.GET.get("role", "user")
        prof, _ = Profile.objects.get_or_create(user=target)
        prof.role = role
        prof.save()
        messages.warning(request, f"Роль пользователя {target.username} изменена (уязвимо) на {role}")
        return redirect("index")
    return HttpResponseForbidden("Admin only")

# SECURE
@login_required
@require_POST
def promote_user_secure(request, user_id):
    if _get_profile(request.user).role != "admin":
        return HttpResponseForbidden("Admin only")
    target = get_object_or_404(User, id=user_id)
    role = request.POST.get("role", "user")
    if role not in ("user", "moderator", "admin"):
        role = "user"
    prof, _ = Profile.objects.get_or_create(user=target)
    prof.role = role
    prof.save()
    messages.success(request, f"Роль пользователя {target.username} изменена (безопасно) на {role}")
    return redirect("index")
