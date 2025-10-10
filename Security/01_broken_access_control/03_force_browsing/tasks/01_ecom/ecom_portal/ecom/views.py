import os
from urllib.parse import unquote
from django.conf import settings
from django.http import Http404, HttpResponse, FileResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator


from ecom.models import Order, InvoiceFile, User


# ---------- Vulnerable demo endpoints (do NOT deploy) ----------
@require_GET
def admin_maintenance(request):
    return HttpResponse("<h1>MAINTENANCE</h1><p>Admin actions (vuln demo)</p>")

@require_GET
def staging_debug(request):
    return HttpResponse("<h1>STAGING DEBUG (vuln)</h1>")

@require_GET
def crash(request):
    user = getattr(request, "user", None)
    if user and getattr(user, "is_authenticated", False) and hasattr(user, "description"):
        info = user.description()
    else:
        info = "anon"
    raise RuntimeError(f"CRASH DEMO - {info} | DEBUG={getattr(settings,'DEBUG',None)}")

@require_GET
def order_view(request, order_id: int):
    """
    Vulnerable: returns order data without ACL checks.
    """
    print(f"requested {order_id}")
    order = get_object_or_404(Order, pk=order_id)
    print(f"founded {order}")
    data = {"id": order.id, "customer": str(order.customer), "total": str(order.total)}
    return JsonResponse(data)

@require_GET
def download_invoice_vuln(request, invoice_id: int):
    invoice = get_object_or_404(InvoiceFile, pk=invoice_id)
    try:
        fp = invoice.file.path
        return FileResponse(open(fp, "rb"), as_attachment=True, filename=invoice.filename or os.path.basename(fp))
    except Exception:
        raise Http404("File not found")

@require_GET
def export_user_profile(request, user_id: int):
    user = get_object_or_404(User, pk=user_id)
    data = {"id": user.id, "username": user.get_username(), "email": user.email}
    return JsonResponse(data)

@require_GET
def download_by_token(request):
    token = unquote(request.GET.get("token", "") or "")
    SIMPLE_TOKEN_MAP = {
        "invoice_1": "invoices/1/invoice1.txt",
        "backup": "backups/db_dump.sql",
    }
    target = SIMPLE_TOKEN_MAP.get(token)
    if not target:
        raise Http404("Not found")
    media_root = getattr(settings, "MEDIA_ROOT", None)
    if not media_root:
        raise Http404("Server misconfigured")
    full = os.path.normpath(os.path.join(media_root, target))
    if not full.startswith(os.path.normpath(media_root)):
        raise Http404("Invalid path")
    if not os.path.exists(full):
        raise Http404("File not found")
    return FileResponse(open(full, "rb"), as_attachment=True, filename=os.path.basename(full))


# ---------- Helpers ----------
def is_shop_manager(user):
    return user.is_authenticated and (getattr(user, "is_mgr", False) or user.is_staff or user.is_superuser)

def is_admin_user(user):
    return user.is_authenticated and (getattr(user, "is_admin", False) or user.is_superuser)


# ---------- Protected / fixed views ----------
@login_required(login_url="ecom:login")
def shop_orders_list(request):
    if not is_shop_manager(request.user):
        return HttpResponseForbidden("Access denied")
    if is_admin_user(request.user):
        qs = Order.objects.all().order_by("-created_at")
    else:
        qs = Order.objects.filter(customer=request.user).order_by("-created_at")
    return render(request, "ecom/list.html", {"orders": qs})

@login_required(login_url="ecom:login")
def shop_order_detail(request, order_id: int):
    order = get_object_or_404(Order, pk=order_id)
    if not (is_admin_user(request.user) or is_shop_manager(request.user) or order.customer == request.user):
        return HttpResponseForbidden("Access denied")
    invoices = order.invoices.all().order_by("-uploaded_at")
    return render(request, "ecom/detail.html", {"order": order, "invoices": invoices})

@login_required(login_url="ecom:login")
def download_invoice_protected(request, invoice_id: int):
    invoice = get_object_or_404(InvoiceFile, pk=invoice_id)
    if hasattr(invoice, "is_accessible_by"):
        allowed = invoice.is_accessible_by(request.user)
    else:
        allowed = is_admin_user(request.user) or (invoice.order.customer == request.user) or is_shop_manager(request.user)
    if not allowed:
        return HttpResponseForbidden("Access denied to file")
    try:
        path = invoice.file.path
    except Exception:
        raise Http404("File not available")
    if not os.path.exists(path):
        raise Http404("File not found")
    return FileResponse(open(path, "rb"), as_attachment=True, filename=invoice.filename or os.path.basename(path))

@login_required(login_url="ecom:login")
def index(request):
    ctx = {"is_mgr": is_shop_manager(request.user), "is_admin": is_admin_user(request.user), "username": request.user.get_username()}
    return render(request, "ecom/index.html", ctx)

@login_required(login_url="ecom:login")
def admin_dashboard(request):
    """
    Admin dashboard for ecom: shows recent orders and recent invoice files,
    with optional search (q) and pagination.
    Template: templates/ecom/admin_dashboard.html
    Context:
      - orders_page (page object)
      - invoices_page (page object)
      - q (search term)
    """
    if not is_admin_user(request.user):
        return HttpResponseForbidden("Access denied: admin only")

    q = request.GET.get("q", "").strip()

    orders_qs = Order.objects.all().order_by("-created_at")
    if q:
        orders_qs = orders_qs.filter(customer__username__icontains=q)  # simple search

    invoices_qs = InvoiceFile.objects.select_related("order").all().order_by("-uploaded_at")
    # optionally filter invoices by filename
    if q:
        invoices_qs = invoices_qs.filter(filename__icontains=q)

    orders_page = Paginator(orders_qs, 25).get_page(request.GET.get("orders_page"))
    invoices_page = Paginator(invoices_qs, 25).get_page(request.GET.get("invoices_page"))

    return render(request, "ecom/admin_dashboard.html", {
        "orders_page": orders_page,
        "invoices_page": invoices_page,
        "q": q,
    })