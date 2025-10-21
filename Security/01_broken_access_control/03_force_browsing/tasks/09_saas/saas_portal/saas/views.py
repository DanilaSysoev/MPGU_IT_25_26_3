import os
from urllib.parse import unquote
from django.conf import settings
from django.http import Http404, HttpResponse, FileResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from saas.models import Project, Task, Attachment, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@require_GET
def admin_maintenance(request): return HttpResponse("<h1>MAINTENANCE (saas)</h1>")
@require_GET
def staging_debug(request): return HttpResponse("<h1>STAGING DEBUG (saas)</h1>")
@require_GET
def crash(request):
    user = getattr(request,"user",None); info = user.description() if user and getattr(user,"is_authenticated",False) and hasattr(user,"description") else "anon"
    raise RuntimeError(f"CRASH: {info} | DEBUG={getattr(settings,'DEBUG',None)}")

@require_GET
def project_view(request, project_id:int):
    p = get_object_or_404(Project, pk=project_id)
    return JsonResponse({"id":p.id,"name":p.name})

@require_GET
def download_attachment_vuln(request, att_id:int):
    att = get_object_or_404(Attachment, pk=att_id)
    try: fp = att.file.path; return FileResponse(open(fp,"rb"), as_attachment=True, filename=att.filename or os.path.basename(fp))
    except: raise Http404("File not found")

@require_GET
def export_user_profile(request, user_id:int):
    u = get_object_or_404(User, pk=user_id); return JsonResponse({"id":u.id,"username":u.get_username(),"email":u.email})

@require_GET
def download_by_token(request):
    token = unquote(request.GET.get("token","") or "")
    SIMPLE_TOKEN_MAP = {"att_1":"attachments/1/a1.pdf","backup":"backups/pm_dump.sql"}
    target = SIMPLE_TOKEN_MAP.get(token); 
    if not target: raise Http404("Not found")
    mr = getattr(settings,"MEDIA_ROOT",None); 
    if not mr: raise Http404("Server misconfigured")
    full = os.path.normpath(os.path.join(mr,target))
    if not full.startswith(os.path.normpath(mr)): raise Http404("Invalid path")
    if not os.path.exists(full): raise Http404("File not found")
    return FileResponse(open(full,"rb"), as_attachment=True, filename=os.path.basename(full))

def is_project_member(user, project):
    return user.is_authenticated and project.members.filter(pk=user.pk).exists()

def is_admin_user(user): return user.is_authenticated and (getattr(user,"is_admin",False) or user.is_superuser)

@login_required(login_url="saas:login")
def projects_list(request):
    qs = Project.objects.filter(members__in=[request.user]).distinct() if not is_admin_user(request.user) else Project.objects.all()
    return render(request,"saas/list.html",{"objects":qs})

@login_required(login_url="saas:login")
def task_detail(request, task_id:int):
    task = get_object_or_404(Task, pk=task_id)
    if not (is_admin_user(request.user) or is_project_member(request.user, task.project)):
        return HttpResponseForbidden("Access denied")
    attachments = task.attachments.all().order_by("-uploaded_at")
    return render(request,"saas/detail.html",{"obj":task,"files":attachments})

@login_required(login_url="saas:login")
def download_attachment(request, att_id:int):
    att = get_object_or_404(Attachment, pk=att_id)
    if hasattr(att,"is_accessible_by"): allowed = att.is_accessible_by(request.user)
    else: allowed = is_admin_user(request.user) or is_project_member(request.user, att.task.project)
    if not allowed: return HttpResponseForbidden("Access denied")
    try: path = att.file.path
    except: raise Http404("File not available")
    if not os.path.exists(path): raise Http404("File not found")
    return FileResponse(open(path,"rb"), as_attachment=True, filename=att.filename or os.path.basename(path))

@login_required(login_url="saas:login")
def admin_dashboard(request):
    if not is_admin_user(request.user): return HttpResponseForbidden("Access denied")
    projects = Project.objects.all()
    return render(request,"saas/admin_dashboard.html",{"projects":projects})

@login_required(login_url="saas:login")
def index(request):
    ctx = {"is_admin": is_admin_user(request.user), "username": request.user.get_username()}
    return render(request,"saas/index.html",ctx)
