import os
from urllib.parse import unquote
from django.conf import settings
from django.http import Http404, HttpResponse, FileResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from legal.models import Case, CaseDocument, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@require_GET
def admin_maintenance(request): return HttpResponse("<h1>MAINTENANCE (legal)</h1>")
@require_GET
def staging_debug(request): return HttpResponse("<h1>STAGING DEBUG (legal)</h1>")
@require_GET
def crash(request):
    user = getattr(request,"user",None); info = user.description() if user and getattr(user,"is_authenticated",False) and hasattr(user,"description") else "anon"
    raise RuntimeError(f"CRASH: {info} | DEBUG={getattr(settings,'DEBUG',None)}")

@require_GET
def case_view(request, case_id:int):
    c = get_object_or_404(Case, pk=case_id)
    return JsonResponse({"id":c.id,"title":c.title,"client":str(c.client)})

@require_GET
def download_case_doc_vuln(request, doc_id:int):
    doc = get_object_or_404(CaseDocument, pk=doc_id)
    try: fp = doc.file.path; return FileResponse(open(fp,"rb"), as_attachment=True, filename=doc.filename or os.path.basename(fp))
    except: raise Http404("File not found")

@require_GET
def export_user_profile(request, user_id:int):
    u = get_object_or_404(User, pk=user_id); return JsonResponse({"id":u.id,"username":u.get_username(),"email":u.email})

@require_GET
def download_by_token(request):
    token = unquote(request.GET.get("token","") or "")
    SIMPLE_TOKEN_MAP = {"case_doc_1":"case_docs/1/doc1.pdf","backup":"backups/legal_dump.sql"}
    target = SIMPLE_TOKEN_MAP.get(token)
    if not target: raise Http404("Not found")
    mr = getattr(settings,"MEDIA_ROOT",None); 
    if not mr: raise Http404("Server misconfigured")
    full = os.path.normpath(os.path.join(mr,target))
    if not full.startswith(os.path.normpath(mr)): raise Http404("Invalid path")
    if not os.path.exists(full): raise Http404("File not found")
    return FileResponse(open(full,"rb"), as_attachment=True, filename=os.path.basename(full))

def is_lawyer(user): return user.is_authenticated and (getattr(user,"is_lawyer",False) or user.is_superuser)
def is_admin_user(user): return user.is_authenticated and (getattr(user,"is_admin",False) or user.is_superuser)

@login_required(login_url="legal:login")
def cases_list(request):
    if is_admin_user(request.user): qs = Case.objects.all().order_by("-created_at")
    else: qs = Case.objects.filter(client=request.user).order_by("-created_at")
    return render(request,"legal/list.html",{"objects":qs})

@login_required(login_url="legal:login")
def case_detail(request, case_id:int):
    c = get_object_or_404(Case, pk=case_id)
    if not (is_admin_user(request.user) or is_lawyer(request.user) or c.client==request.user): return HttpResponseForbidden("Access denied")
    docs = c.documents.all().order_by("-uploaded_at")
    return render(request,"legal/detail.html",{"case":c,"docs":docs})

@login_required(login_url="legal:login")
def download_case_doc(request, doc_id:int):
    doc = get_object_or_404(CaseDocument, pk=doc_id)
    if hasattr(doc,"is_accessible_by"): allowed = doc.is_accessible_by(request.user)
    else: allowed = is_admin_user(request.user) or is_lawyer(request.user) or doc.case.client==request.user
    if not allowed: return HttpResponseForbidden("Access denied")
    try: path = doc.file.path
    except: raise Http404("File not available")
    if not os.path.exists(path): raise Http404("File not found")
    return FileResponse(open(path,"rb"), as_attachment=True, filename=doc.filename or os.path.basename(path))

@login_required(login_url="legal:login")
def admin_dashboard(request):
    if not is_admin_user(request.user): return HttpResponseForbidden("Access denied")
    cases = Case.objects.all()
    return render(request,"legal/admin_dashboard.html",{"cases":cases})

@login_required(login_url="legal:login")
def index(request):
    ctx = {"is_lawyer": is_lawyer(request.user), "is_admin": is_admin_user(request.user), "username": request.user.get_username()}
    return render(request,"legal/index.html",ctx)
