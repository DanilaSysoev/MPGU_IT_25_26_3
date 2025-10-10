import os
from urllib.parse import unquote
from django.conf import settings
from django.http import Http404, HttpResponse, FileResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from real_estate.models import Listing, DocFile, User


@require_GET
def admin_maintenance(request): return HttpResponse("<h1>MAINTENANCE (real_estate)</h1>")
@require_GET
def staging_debug(request): return HttpResponse("<h1>STAGING DEBUG (real_estate)</h1>")
@require_GET
def crash(request):
    user = getattr(request,"user",None); info = user.description() if user and getattr(user,"is_authenticated",False) and hasattr(user,"description") else "anon"
    raise RuntimeError(f"CRASH: {info} | DEBUG={getattr(settings,'DEBUG',None)}")

@require_GET
def listing_view(request, listing_id:int):
    l = get_object_or_404(Listing, pk=listing_id)
    return JsonResponse({"id":l.id,"title":l.title,"owner":str(l.owner),"published":l.is_published})

@require_GET
def download_doc_vuln(request, doc_id:int):
    doc = get_object_or_404(DocFile, pk=doc_id)
    try: fp = doc.file.path; return FileResponse(open(fp,"rb"), as_attachment=True, filename=doc.filename or os.path.basename(fp))
    except: raise Http404("File not found")

@require_GET
def export_user_profile(request, user_id:int):
    u = get_object_or_404(User, pk=user_id)
    return JsonResponse({"id":u.id,"username":u.get_username(),"email":u.email})

@require_GET
def download_by_token(request):
    token = unquote(request.GET.get("token","") or "")
    SIMPLE_TOKEN_MAP = {"doc_1":"docs/1/doc1.pdf","backup":"backups/real_estate.sql"}
    target = SIMPLE_TOKEN_MAP.get(token); 
    if not target: raise Http404("Not found")
    mr = getattr(settings,"MEDIA_ROOT",None); 
    if not mr: raise Http404("Server misconfigured")
    full = os.path.normpath(os.path.join(mr,target))
    if not full.startswith(os.path.normpath(mr)): raise Http404("Invalid path")
    if not os.path.exists(full): raise Http404("File not found")
    return FileResponse(open(full,"rb"), as_attachment=True, filename=os.path.basename(full))

def is_agent(user): return user.is_authenticated and (getattr(user,"is_agent",False) or user.is_superuser)
def is_admin_user(user): return user.is_authenticated and (getattr(user,"is_admin",False) or user.is_superuser)

@login_required(login_url="real_estate:login")
def listings_list(request):
    if is_admin_user(request.user): qs = Listing.objects.all().order_by("-id")
    else: qs = Listing.objects.filter(owner=request.user).order_by("-id")
    return render(request,"real_estate/list.html",{"listings":qs})

@login_required(login_url="real_estate:login")
def listing_detail(request, listing_id:int):
    l = get_object_or_404(Listing, pk=listing_id)
    if not (is_admin_user(request.user) or l.owner==request.user or is_agent(request.user)):
        return HttpResponseForbidden("Access denied")
    docs = l.docs.all().order_by("-uploaded_at")
    return render(request,"real_estate/detail.html",{"listing":l,"docs":docs})

@login_required(login_url="real_estate:login")
def download_doc(request, doc_id:int):
    doc = get_object_or_404(DocFile, pk=doc_id)
    if hasattr(doc,"is_accessible_by"): allowed = doc.is_accessible_by(request.user)
    else: allowed = is_admin_user(request.user) or doc.listing.owner==request.user or is_agent(request.user)
    if not allowed: return HttpResponseForbidden("Access denied")
    try: path = doc.file.path
    except: raise Http404("File not available")
    if not os.path.exists(path): raise Http404("File not found")
    return FileResponse(open(path,"rb"), as_attachment=True, filename=doc.filename or os.path.basename(path))

@login_required(login_url="real_estate:login")
def admin_dashboard(request):
    if not is_admin_user(request.user): return HttpResponseForbidden("Access denied")
    listings = Listing.objects.all()
    return render(request,"real_estate/admin_dashboard.html",{"listings":listings})

@login_required(login_url="real_estate:login")
def index(request):
    ctx = {"is_agent": is_agent(request.user), "is_admin": is_admin_user(request.user), "username": request.user.get_username()}
    return render(request,"real_estate/index.html", ctx)
