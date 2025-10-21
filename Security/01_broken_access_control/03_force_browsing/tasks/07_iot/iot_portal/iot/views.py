import os
from urllib.parse import unquote
from django.conf import settings
from django.http import Http404, HttpResponse, FileResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from iot.models import Device, LogFile, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@require_GET
def admin_maintenance(request): return HttpResponse("<h1>MAINTENANCE (iot)</h1>")
@require_GET
def staging_debug(request): return HttpResponse("<h1>STAGING DEBUG (iot)</h1>")
@require_GET
def crash(request):
    user = getattr(request,"user",None)
    info = user.description() if user and getattr(user,"is_authenticated",False) and hasattr(user,"description") else "anon"
    raise RuntimeError(f"CRASH: {info} | DEBUG={getattr(settings,'DEBUG',None)}")

@require_GET
def device_view(request, device_id:int):
    d = get_object_or_404(Device, pk=device_id)
    return JsonResponse({"id":d.id,"serial":d.serial,"owner":str(d.owner)})

@require_GET
def download_log_vuln(request, log_id:int):
    lf = get_object_or_404(LogFile, pk=log_id)
    try: fp = lf.file.path; return FileResponse(open(fp,"rb"), as_attachment=True, filename=lf.filename or os.path.basename(fp))
    except: raise Http404("File not found")

@require_GET
def export_user_profile(request, user_id:int):
    u = get_object_or_404(User, pk=user_id); return JsonResponse({"id":u.id,"username":u.get_username(),"email":u.email})

@require_GET
def download_by_token(request):
    token = unquote(request.GET.get("token","") or "")
    SIMPLE_TOKEN_MAP = {"log_1":"logs/1/log1.txt","backup":"backups/iot_dump.sql"}
    target = SIMPLE_TOKEN_MAP.get(token); 
    if not target: raise Http404("Not found")
    mr = getattr(settings,"MEDIA_ROOT",None); 
    if not mr: raise Http404("Server misconfigured")
    full = os.path.normpath(os.path.join(mr,target))
    if not full.startswith(os.path.normpath(mr)): raise Http404("Invalid path")
    if not os.path.exists(full): raise Http404("File not found")
    return FileResponse(open(full,"rb"), as_attachment=True, filename=os.path.basename(full))

def is_tech(user): return user.is_authenticated and (getattr(user,"is_tech",False) or user.is_superuser)
def is_admin_user(user): return user.is_authenticated and (getattr(user,"is_admin",False) or user.is_superuser)

@login_required(login_url="iot:login")
def devices_list(request):
    if is_admin_user(request.user): qs = Device.objects.all().order_by("-id")
    else: qs = Device.objects.filter(owner=request.user).order_by("-id")
    return render(request,"iot/list.html",{"objects":qs})

@login_required(login_url="iot:login")
def device_detail(request, device_id:int):
    d = get_object_or_404(Device, pk=device_id)
    if not (is_admin_user(request.user) or is_tech(request.user) or d.owner==request.user): return HttpResponseForbidden("Access denied")
    logs = d.logs.all().order_by("-created_at")
    return render(request,"iot/detail.html",{"obj":d,"files":logs})

@login_required(login_url="iot:login")
def download_log(request, log_id:int):
    lf = get_object_or_404(LogFile, pk=log_id)
    if hasattr(lf,"is_accessible_by"): allowed = lf.is_accessible_by(request.user)
    else: allowed = is_admin_user(request.user) or lf.device.owner==request.user or is_tech(request.user)
    if not allowed: return HttpResponseForbidden("Access denied")
    try: path = lf.file.path
    except: raise Http404("File not available")
    if not os.path.exists(path): raise Http404("File not found")
    return FileResponse(open(path,"rb"), as_attachment=True, filename=lf.filename or os.path.basename(path))

@login_required(login_url="iot:login")
def admin_dashboard(request):
    if not is_admin_user(request.user): return HttpResponseForbidden("Access denied")
    devices = Device.objects.all()
    return render(request,"iot/admin_dashboard.html",{"devices":devices})

@login_required(login_url="iot:login")
def index(request):
    ctx = {"is_tech": is_tech(request.user), "is_admin": is_admin_user(request.user), "username": request.user.get_username()}
    return render(request,"iot/index.html",ctx)
