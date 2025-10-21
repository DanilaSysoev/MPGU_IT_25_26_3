import os
from urllib.parse import unquote
from django.conf import settings
from django.http import Http404, HttpResponse, FileResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from fintech.models import Account, Statement, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@require_GET
def admin_maintenance(request): return HttpResponse("<h1>MAINTENANCE (fintech)</h1>")
@require_GET
def staging_debug(request): return HttpResponse("<h1>STAGING DEBUG (fintech)</h1>")
@require_GET
def crash(request):
    user = getattr(request,"user",None); info = user.description() if user and getattr(user,"is_authenticated",False) and hasattr(user,"description") else "anon"
    raise RuntimeError(f"CRASH: {info} | DEBUG={getattr(settings,'DEBUG',None)}")

@require_GET
def account_view(request, account_id:int):
    acc = get_object_or_404(Account, pk=account_id)
    return JsonResponse({"id":acc.id,"number":acc.number,"owner":str(acc.owner)})

@require_GET
def download_statement_vuln(request, statement_id:int):
    st = get_object_or_404(Statement, pk=statement_id)
    try: fp = st.file.path; return FileResponse(open(fp,"rb"), as_attachment=True, filename=st.filename or os.path.basename(fp))
    except: raise Http404("File not found")

@require_GET
def export_user_profile(request, user_id:int):
    u = get_object_or_404(User, pk=user_id)
    return JsonResponse({"id":u.id,"username":u.get_username(),"email":u.email})

@require_GET
def download_by_token(request):
    token = unquote(request.GET.get("token","") or "")
    SIMPLE_TOKEN_MAP = {"stmt_1":"statements/1/stmt1.pdf","backup":"backups/bank_dump.sql"}
    target = SIMPLE_TOKEN_MAP.get(token); 
    if not target: raise Http404("Not found")
    mr = getattr(settings,"MEDIA_ROOT",None); 
    if not mr: raise Http404("Server misconfigured")
    full = os.path.normpath(os.path.join(mr,target))
    if not full.startswith(os.path.normpath(mr)): raise Http404("Invalid path")
    if not os.path.exists(full): raise Http404("File not found")
    return FileResponse(open(full,"rb"), as_attachment=True, filename=os.path.basename(full))

def is_teller(user):
    return user.is_authenticated and (getattr(user,"is_teller",False) or user.is_staff or user.is_superuser)
def is_admin_user(user):
    return user.is_authenticated and (getattr(user,"is_admin",False) or user.is_superuser)

@login_required(login_url="fintech:login")
def accounts_list(request):
    if not is_teller(request.user): return HttpResponseForbidden("Access denied")
    if is_admin_user(request.user): qs = Account.objects.all().order_by("-id")
    else: qs = Account.objects.filter(owner=request.user).order_by("-id")
    return render(request, "fintech/list.html", {"objects":qs})

@login_required(login_url="fintech:login")
def account_detail(request, account_id:int):
    acc = get_object_or_404(Account, pk=account_id)
    if not (is_admin_user(request.user) or is_teller(request.user) or acc.owner==request.user): return HttpResponseForbidden("Access denied")
    statements = acc.statements.all().order_by("-created_at")
    return render(request, "fintech/detail.html", {"obj":acc,"filed":statements})

@login_required(login_url="fintech:login")
def download_statement(request, statement_id:int):
    st = get_object_or_404(Statement, pk=statement_id)
    if hasattr(st,"is_accessible_by"): allowed = st.is_accessible_by(request.user)
    else: allowed = is_admin_user(request.user) or st.account.owner==request.user or is_teller(request.user)
    if not allowed: return HttpResponseForbidden("Access denied")
    try: path = st.file.path
    except: raise Http404("File not available")
    if not os.path.exists(path): raise Http404("File not found")
    return FileResponse(open(path,"rb"), as_attachment=True, filename=st.filename or os.path.basename(path))

@login_required(login_url="fintech:login")
def admin_dashboard(request):
    if not is_admin_user(request.user): return HttpResponseForbidden("Access denied")
    accounts = Account.objects.all()
    return render(request,"fintech/admin_dashboard.html",{"accounts":accounts})

@login_required(login_url="fintech:login")
def index(request):
    ctx = {"is_teller": is_teller(request.user), "is_admin": is_admin_user(request.user), "username": request.user.get_username()}
    return render(request,"fintech/index.html",ctx)
