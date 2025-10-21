import os
from urllib.parse import unquote
from django.conf import settings
from django.http import Http404, HttpResponse, FileResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model

from lms.models import Course, Assignment, Submission, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



@require_GET
def admin_maintenance(request): return HttpResponse("<h1>MAINTENANCE (lms)</h1>")
@require_GET
def staging_debug(request): return HttpResponse("<h1>STAGING DEBUG (lms)</h1>")
@require_GET
def crash(request):
    user = getattr(request,"user",None)
    info = user.description() if user and getattr(user,"is_authenticated",False) and hasattr(user,"description") else "anon"
    raise RuntimeError(f"CRASH: {info} | DEBUG={getattr(settings,'DEBUG',None)}")

@require_GET
def assignment_view(request, assignment_id:int):
    a = get_object_or_404(Assignment, pk=assignment_id)
    return JsonResponse({"id":a.id,"title":a.title,"course":str(a.course)})

@require_GET
def download_submission_vuln(request, submission_id:int):
    sub = get_object_or_404(Submission, pk=submission_id)
    try:
        fp = sub.file.path
        return FileResponse(open(fp,"rb"), as_attachment=True, filename=sub.filename or os.path.basename(fp))
    except Exception:
        raise Http404("File not found")

@require_GET
def export_user_profile(request, user_id:int):
    u = get_object_or_404(User, pk=user_id)
    return JsonResponse({"id":u.id,"username":u.get_username(),"email":u.email})

@require_GET
def download_by_token(request):
    token = unquote(request.GET.get("token","") or "")
    SIMPLE_TOKEN_MAP = {"sub_1":"submissions/1/sub1.txt","backup":"backups/lms.sql"}
    target = SIMPLE_TOKEN_MAP.get(token); 
    if not target: raise Http404("Not found")
    mr = getattr(settings,"MEDIA_ROOT",None); 
    if not mr: raise Http404("Server misconfigured")
    full = os.path.normpath(os.path.join(mr,target))
    if not full.startswith(os.path.normpath(mr)): raise Http404("Invalid path")
    if not os.path.exists(full): raise Http404("File not found")
    return FileResponse(open(full,"rb"), as_attachment=True, filename=os.path.basename(full))

def is_instructor(user):
    return user.is_authenticated and (getattr(user,"is_instructor",False) or user.is_superuser)

def is_admin_user(user):
    return user.is_authenticated and (getattr(user,"is_admin",False) or user.is_superuser)

@login_required(login_url="lms:login")
def instructor_assignments(request):
    if not is_instructor(request.user): return HttpResponseForbidden("Access denied")
    if is_admin_user(request.user): qs = Assignment.objects.all().order_by("-id")
    else: qs = Assignment.objects.filter(course__in=request.user.courses_instructed.all()).order_by("-id")
    return render(request, "lms/list.html", {"objects":qs})

@login_required(login_url="lms:login")
def submission_detail(request, submission_id:int):
    sub = get_object_or_404(Submission, pk=submission_id)
    if not (is_admin_user(request.user) or sub.student == request.user or sub.assignment.course.instructors.filter(pk=request.user.pk).exists()):
        return HttpResponseForbidden("Access denied")
    return render(request, "lms/detail.html", {"submission":sub})

@login_required(login_url="lms:login")
def download_submission(request, submission_id:int):
    sub = get_object_or_404(Submission, pk=submission_id)
    if hasattr(sub,"is_accessible_by"):
        allowed = sub.is_accessible_by(request.user)
    else:
        allowed = is_admin_user(request.user) or sub.student==request.user or sub.assignment.course.instructors.filter(pk=request.user.pk).exists()
    if not allowed: return HttpResponseForbidden("Access denied")
    try: path = sub.file.path
    except: raise Http404("File not available")
    if not os.path.exists(path): raise Http404("File not found")
    return FileResponse(open(path,"rb"), as_attachment=True, filename=sub.filename or os.path.basename(path))

@login_required(login_url="lms:login")
def admin_dashboard(request):
    if not is_admin_user(request.user): return HttpResponseForbidden("Access denied")
    courses = Course.objects.all()
    return render(request, "lms/admin_dashboard.html", {"courses":courses})

@login_required(login_url="lms:login")
def index(request):
    ctx = {"is_instructor": is_instructor(request.user), "is_admin": is_admin_user(request.user), "username": request.user.get_username()}
    return render(request, "lms/index.html", ctx)
