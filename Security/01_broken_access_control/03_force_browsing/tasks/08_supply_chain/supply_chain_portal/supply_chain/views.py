import os
from urllib.parse import unquote
from django.conf import settings
from django.http import Http404, HttpResponse, FileResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from supply_chain.models import InventoryItem, ShipmentDocument, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@require_GET
def admin_maintenance(request): return HttpResponse("<h1>MAINTENANCE (supply_chain)</h1>")
@require_GET
def staging_debug(request): return HttpResponse("<h1>STAGING DEBUG (supply_chain)</h1>")
@require_GET
def crash(request):
    user = getattr(request,"user",None); info = user.description() if user and getattr(user,"is_authenticated",False) and hasattr(user,"description") else "anon"
    raise RuntimeError(f"CRASH: {info} | DEBUG={getattr(settings,'DEBUG',None)}")

@require_GET
def item_view(request, item_id:int):
    it = get_object_or_404(InventoryItem, pk=item_id)
    return JsonResponse({"id":it.id,"sku":it.sku,"supplier":str(it.supplier)})

@require_GET
def download_shipment_doc_vuln(request, doc_id:int):
    doc = get_object_or_404(ShipmentDocument, pk=doc_id)
    try: fp = doc.file.path; return FileResponse(open(fp,"rb"), as_attachment=True, filename=doc.filename or os.path.basename(fp))
    except: raise Http404("File not found")

@require_GET
def export_user_profile(request, user_id:int):
    u = get_object_or_404(User, pk=user_id); return JsonResponse({"id":u.id,"username":u.get_username(),"email":u.email})

@require_GET
def download_by_token(request):
    token = unquote(request.GET.get("token","") or "")
    SIMPLE_TOKEN_MAP = {"ship_1":"shipments/1/doc1.pdf","backup":"backups/inventory_dump.sql"}
    target = SIMPLE_TOKEN_MAP.get(token); 
    if not target: raise Http404("Not found")
    mr = getattr(settings,"MEDIA_ROOT",None); 
    if not mr: raise Http404("Server misconfigured")
    full = os.path.normpath(os.path.join(mr,target))
    if not full.startswith(os.path.normpath(mr)): raise Http404("Invalid path")
    if not os.path.exists(full): raise Http404("File not found")
    return FileResponse(open(full,"rb"), as_attachment=True, filename=os.path.basename(full))

def is_supply_manager(user): return user.is_authenticated and (getattr(user,"is_supply_manager",False) or user.is_superuser)
def is_admin_user(user): return user.is_authenticated and (getattr(user,"is_admin",False) or user.is_superuser)

@login_required(login_url="supply_chain:login")
def items_list(request):
    if is_admin_user(request.user): qs = InventoryItem.objects.all().order_by("-id")
    else: qs = InventoryItem.objects.filter(supplier__items__isnull=False).order_by("-id")
    return render(request,"supply_chain/list.html",{"objects":qs})

@login_required(login_url="supply_chain:login")
def item_detail(request, item_id:int):
    it = get_object_or_404(InventoryItem, pk=item_id)
    if not (is_admin_user(request.user) or is_supply_manager(request.user)):
        return HttpResponseForbidden("Access denied")
    docs = it.docs.all().order_by("-created_at")
    return render(request,"supply_chain/detail.html",{"item":it,"docs":docs})

@login_required(login_url="supply_chain:login")
def download_shipment_doc(request, doc_id:int):
    doc = get_object_or_404(ShipmentDocument, pk=doc_id)
    if hasattr(doc,"is_accessible_by"): allowed = doc.is_accessible_by(request.user)
    else: allowed = is_admin_user(request.user) or is_supply_manager(request.user)
    if not allowed: return HttpResponseForbidden("Access denied")
    try: path = doc.file.path
    except: raise Http404("File not available")
    if not os.path.exists(path): raise Http404("File not found")
    return FileResponse(open(path,"rb"), as_attachment=True, filename=doc.filename or os.path.basename(path))

@login_required(login_url="supply_chain:login")
def admin_dashboard(request):
    if not is_admin_user(request.user): return HttpResponseForbidden("Access denied")
    items = InventoryItem.objects.all()
    return render(request,"supply_chain/admin_dashboard.html",{"items":items})

@login_required(login_url="supply_chain:login")
def index(request):
    ctx = {"is_supply_manager": is_supply_manager(request.user), "is_admin": is_admin_user(request.user), "username": request.user.get_username()}
    return render(request,"supply_chain/index.html",ctx)
