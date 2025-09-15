from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm
from .models import Booking ,Payment
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

def index(request):
    my_lists = [("/secure/booking/list/","Booking: мои объекты"), ("/secure/payment/list/","Payment: мои объекты")]
    return render(request, "index.html", {"my_lists": my_lists, "domain_desc": "Бронирования и платежи"})

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
def booking_list(request):
    objs = Booking.objects.filter(owner=request.user).order_by("-id")
    return render(request, "bookingapp/booking_list.html", {"objects": objs})

def booking_detail_vuln(request):
    obj_id = request.GET.get("id")
    obj = get_object_or_404(Booking, id=obj_id)
    return render(request, "bookingapp/booking_detail.html", {"obj": obj, "mode": "vuln_query"})

@login_required
def booking_detail_secure(request, obj_id):
    obj = get_object_or_404(Booking, id=obj_id, owner=request.user)
    return render(request, "bookingapp/booking_detail.html", {"obj": obj, "mode": "secure"})

def booking_detail_vuln_path(request, obj_id):
    obj = get_object_or_404(Booking, id=obj_id)
    return render(request, "bookingapp/booking_detail.html", {"obj": obj, "mode": "vuln_path"})

@require_POST
def booking_update_vuln(request, obj_id):
    obj = get_object_or_404(Booking, id=obj_id)
    if 'title' in request.POST:
        setattr(obj, 'title', request.POST['title'])
    obj.save()
    return redirect("index")



@login_required
def payment_list(request):
    objs = Payment.objects.filter(owner=request.user).order_by("-id")
    return render(request, "bookingapp/payment_list.html", {"objects": objs})

def payment_detail_vuln(request):
    obj_id = request.GET.get("id")
    obj = get_object_or_404(Payment, id=obj_id)
    return render(request, "bookingapp/payment_detail.html", {"obj": obj, "mode": "vuln_query"})

@login_required
def payment_detail_secure(request, obj_id):
    obj = get_object_or_404(Payment, id=obj_id, owner=request.user)
    return render(request, "bookingapp/payment_detail.html", {"obj": obj, "mode": "secure"})

def payment_detail_vuln_path(request, obj_id):
    obj = get_object_or_404(Payment, id=obj_id)
    return render(request, "bookingapp/payment_detail.html", {"obj": obj, "mode": "vuln_path"})

@require_POST
def payment_update_vuln(request, obj_id):
    obj = get_object_or_404(Payment, id=obj_id)
    if 'title' in request.POST:
        setattr(obj, 'title', request.POST['title'])
    obj.save()
    return redirect("index")
