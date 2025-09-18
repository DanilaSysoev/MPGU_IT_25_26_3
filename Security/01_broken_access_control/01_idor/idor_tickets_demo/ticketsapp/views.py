from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm
from .models import Ticket ,Message

def index(request):
    my_lists = [("/secure/ticket/list/","Ticket: мои объекты"), ("/secure/message/list/","Message: мои объекты")]
    return render(request, "index.html", {"my_lists": my_lists, "domain_desc": "Тикеты и сообщения поддержки"})

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
def ticket_list(request):
    objs = Ticket.objects.filter(owner=request.user).order_by("-id")
    return render(request, "ticketsapp/ticket_list.html", {"objects": objs})

def ticket_detail_vuln(request):
    obj_id = request.GET.get("id")
    obj = get_object_or_404(Ticket, id=obj_id)
    if obj.owner == request.user:
        return render(request, "ticketsapp/ticket_detail.html", {"obj": obj, "mode": "vuln_query"})
    else:
        return HttpResponse("Forbidden", status=403)

@login_required
def ticket_detail_secure(request, obj_id):
    obj = get_object_or_404(Ticket, id=obj_id, owner=request.user)
    return render(request, "ticketsapp/ticket_detail.html", {"obj": obj, "mode": "secure"})

def ticket_detail_vuln_path(request, obj_id):
    obj = get_object_or_404(Ticket, id=obj_id)
    if obj.owner == request.user:
        return render(request, "ticketsapp/ticket_detail.html", {"obj": obj, "mode": "vuln_path"})
    else:
        return HttpResponse("Forbidden", status=403)

@require_POST
def ticket_update_vuln(request, obj_id):
    obj = get_object_or_404(Ticket, id=obj_id)
    if obj.owner == request.user:
        if 'title' in request.POST:
            setattr(obj, 'title', request.POST['title'])
        obj.save()
        return redirect("index")
    else:        
        return HttpResponse("Forbidden", status=403)


from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

@login_required
def message_list(request):
    objs = Message.objects.filter(owner=request.user).order_by("-id")
    return render(request, "ticketsapp/message_list.html", {"objects": objs})

def message_detail_vuln(request):
    obj_id = request.GET.get("id")
    obj = get_object_or_404(Message, id=obj_id)
    if obj.owner == request.user:
        return render(request, "ticketsapp/message_detail.html", {"obj": obj, "mode": "vuln_query"})
    else:
        return HttpResponse("Forbidden", status=403)

@login_required
def message_detail_secure(request, obj_id):
    obj = get_object_or_404(Message, id=obj_id, owner=request.user)
    return render(request, "ticketsapp/message_detail.html", {"obj": obj, "mode": "secure"})

def message_detail_vuln_path(request, obj_id):
    obj = get_object_or_404(Message, id=obj_id)
    if obj.owner == request.user:
        return render(request, "ticketsapp/message_detail.html", {"obj": obj, "mode": "vuln_path"})
    else:
        return HttpResponse("Forbidden", status=403)

@require_POST
def message_update_vuln(request, obj_id):    
    obj = get_object_or_404(Message, id=obj_id)
    if obj.owner == request.user:
        if 'text' in request.POST:
            setattr(obj, 'text', request.POST['text'])
        obj.save()
        return redirect("index")
    else:
        return HttpResponse("Forbidden", status=403)
