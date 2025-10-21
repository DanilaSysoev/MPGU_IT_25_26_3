import os
from urllib.parse import unquote
from django.conf import settings
from django.http import Http404, HttpResponse, FileResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from med.models import Patient, MedicalReport, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@require_GET
def admin_maintenance(request):
    return HttpResponse("<h1>MAINTENANCE (med)</h1>")

@require_GET
def staging_debug(request):
    return HttpResponse("<h1>STAGING DEBUG (med)</h1>")

@require_GET
def crash(request):
    user = getattr(request, "user", None)
    info = user.description() if user and getattr(user, "is_authenticated", False) and hasattr(user, "description") else "anon"
    raise RuntimeError(f"CRASH: {info} | DEBUG={getattr(settings,'DEBUG',None)}")

@require_GET
def patient_view(request, patient_id: int):
    patient = get_object_or_404(Patient, pk=patient_id)
    data = {"id": patient.id, "full_name": patient.full_name, "dob": patient.dob.isoformat()}
    return JsonResponse(data)

@require_GET
def download_report_vuln(request, report_id: int):
    report = get_object_or_404(MedicalReport, pk=report_id)
    try:
        fp = report.file.path
        return FileResponse(open(fp, "rb"), as_attachment=True, filename=report.filename or os.path.basename(fp))
    except Exception:
        raise Http404("File not found")

@require_GET
def export_user_profile(request, user_id: int):
    user = get_object_or_404(User, pk=user_id)
    return JsonResponse({"id": user.id, "username": user.get_username(), "email": user.email})

@require_GET
def download_by_token(request):
    token = unquote(request.GET.get("token","") or "")
    SIMPLE_TOKEN_MAP = {"report_1":"reports/1/report1.pdf","backup":"backups/clinic_dump.sql"}
    target = SIMPLE_TOKEN_MAP.get(token)
    if not target: raise Http404("Not found")
    media_root = getattr(settings,"MEDIA_ROOT",None) 
    if not media_root: raise Http404("Server misconfigured")
    full = os.path.normpath(os.path.join(media_root,target))
    if not full.startswith(os.path.normpath(media_root)): raise Http404("Invalid path")
    if not os.path.exists(full): raise Http404("File not found")
    return FileResponse(open(full,"rb"), as_attachment=True, filename=os.path.basename(full))

def is_doctor_user(user):
    return user.is_authenticated and (getattr(user,"is_doctor",False) or user.is_superuser)

def is_admin_user(user):
    return user.is_authenticated and (getattr(user,"is_admin",False) or user.is_superuser)

@login_required(login_url="med:login")
def clinic_patients_list(request):
    if not is_doctor_user(request.user):
        return HttpResponseForbidden("Access denied: doctors only")
    if is_admin_user(request.user):
        qs = Patient.objects.all().order_by("-id")
    else:
        qs = Patient.objects.filter(created_by=request.user).order_by("-id")
    return render(request, "med/list.html", {"objects": qs})

@login_required(login_url="med:login")
def clinic_patient_detail(request, patient_id:int):
    p = get_object_or_404(Patient, pk=patient_id)
    if not (is_admin_user(request.user) or is_doctor_user(request.user) or p.created_by == request.user):
        return HttpResponseForbidden("Access denied")
    reports = p.reports.all().order_by("-created_at")
    return render(request, "med/detail.html", {"obj": p, "files": reports})

@login_required(login_url="med:login")
def download_report_protected(request, report_id:int):
    report = get_object_or_404(MedicalReport, pk=report_id)
    if hasattr(report, "is_accessible_by"):
        allowed = report.is_accessible_by(request.user)
    else:
        allowed = is_admin_user(request.user) or is_doctor_user(request.user) or (report.patient.created_by == request.user)
    if not allowed: return HttpResponseForbidden("Access denied to file")
    try:
        path = report.file.path
    except Exception:
        raise Http404("File not available")
    if not os.path.exists(path): raise Http404("File not found")
    return FileResponse(open(path,"rb"), as_attachment=True, filename=report.filename or os.path.basename(path))

@login_required(login_url="med:login")
def admin_dashboard(request):
    if not is_admin_user(request.user):
        return HttpResponseForbidden("Access denied")
    patients = Patient.objects.all()
    reports = MedicalReport.objects.select_related("patient").order_by("-created_at")
    return render(request, "med/admin_dashboard.html", {"patients":patients, "reports":reports})

@login_required(login_url="med:login")
def index(request):
    ctx = {"is_doctor": is_doctor_user(request.user), "is_admin": is_admin_user(request.user), "username": request.user.get_username()}
    return render(request, "med/index.html", ctx)
