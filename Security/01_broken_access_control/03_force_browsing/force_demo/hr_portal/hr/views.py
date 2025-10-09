import os
from urllib.parse import unquote

from django.conf import settings
from django.http import (
    Http404,
    HttpResponse,
    FileResponse,
    JsonResponse,
)
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET

from hr.models import Candidate, ResumeFile, User

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render

# --------------------------------------------------------------------
# ВНИМАНИЕ (для преподавателя / разработчика):
# Эти view — **vulnerable** (намеренно). Они демонстрируют типичные ошибки.
# Не деплой в продакшен. В комментариях показаны рекомендации по фиксу.
# --------------------------------------------------------------------


@require_GET
def admin_maintenance(request):
    """
    /admin/maintenance
    ------------------
    Уязвимость: нет проверки авторизации -> любой может увидеть админскую страницу.
    Демонстрационная логика — просто возвращаем строку с "админскими" действиями.

    Исправление (fixed): добавить серверную проверку (require_login + require_admin)
    либо использовать Django admin с корректной настройкой прав.
    """
    # vuln: отсутствует проверка request.user.is_authenticated / is_admin
    return HttpResponse(
        "<h1>MAINTENANCE</h1><p>Admin-only actions would be here (vulnerable demo).</p>"
    )


@require_GET
def staging_debug(request):
    """
    /staging/debug
    --------------
    Уязвимость: оставлен тестовый/стендовый роут доступный всем.
    Часто такие страницы содержат диагностическую информацию и служебные ссылки.

    Исправление: убрать из рабочей ветки; включать только при DEBUG=True и/или по флагу,
    и всегда защищать проверкой хоста/права.
    """
    return HttpResponse("<h1>STAGING / DEBUG PAGE</h1><p>Should not be public.</p>")


@require_GET
def crash(request):
    """
    /crash
    ------
    Демонстрационный маршрут, который поднимает исключение с отладочной информацией.
    В vuln-ветке при DEBUG=True Django покажет страницу с этим сообщением — наглядная демонстрация риска.

    НЕЛЬЗЯ оставлять такое в проде: сообщение может содержать PII, конфигурационные данные и т.д.
    """
    # Формируем сообщение с информацией о пользователе (если он есть)
    user = getattr(request, "user", None)
    if user and getattr(user, "is_authenticated", False):
        # include_candidates=True — включаем список кандидатов для HR
        info = user.description(include_candidates=True)
    else:
        info = "anon"

    # Дополнительный контекст (можно добавить любые поля, но осторожно с секретами)
    context = f"CRASH DEMO — debug info: {info} | DEBUG={getattr(settings, 'DEBUG', None)}"

    # Бросаем исключение с этим сообщением (в vuln-ветке при DEBUG=True оно покажется на странице ошибки)
    raise RuntimeError(context)


@require_GET
def candidate_view(request, candidate_id: int):
    """
    /candidates/<id>/
    -----------------
    Уязвимость: нет проверки, что текущий пользователь имеет право смотреть данного кандидата.
    Демонстрационно — возвращаем JSON профиля.

    Исправление:
      - require login (если профиль приватный)
      - проверять created_by / ACL: only owner / HR / admin can view
      - для публичных профилей использовать is_public флаг
    """
    cand = get_object_or_404(Candidate, pk=candidate_id)
    # vuln: возвращаем данные без проверки request.user
    data = {
        "id": cand.id,
        "full_name": cand.full_name,
        "email": cand.email,
        "phone": cand.phone,
        "created_by": cand.created_by.get_username() if cand.created_by else None,
    }
    return JsonResponse(data)


@require_GET
def download_resume(request, resume_id: int):
    """
    storage/files/<id>/download/
    ---------------------
    Уязвимость: отдаём файл по ID без проверки владения/прав.
    Файлы хранятся через Django FileField — но контроль доступа должен быть на уровне view.

    Исправление:
      - потребовать авторизацию
      - проверить resume.is_accessible_by(request.user)
      - отдавать файл через FileResponse только после проверки
      - хранить приватные файлы вне публичного static/serve путей
    """
    resume = get_object_or_404(ResumeFile, pk=resume_id)
    # vuln: нет проверки прав
    try:
        # используем file.path — в реальности убедитесь, что поле имеет путь
        fp = resume.file.path
        return FileResponse(open(fp, "rb"), as_attachment=True, filename=resume.filename or os.path.basename(fp))
    except Exception:
        raise Http404("File not found")


@require_GET
def export_user_profile(request, user_id: int):
    """
    /api/users/<id>/export
    ---------------------
    Уязвимость: экспорт профиля — без проверки прав. Любой, кто знает ID, получит данные.

    Исправление:
      - требовать аутентификацию
      - проверять is_admin или что запрашиваемый профиль принадлежит текущему пользователю
    """
    user = get_object_or_404(User, pk=user_id)
    # vuln: no auth / no check
    data = {
        "id": user.id,
        "username": user.get_username(),
        "email": user.email,
        # не включать секреты/хэши паролей!
    }
    return JsonResponse(data)


@require_GET
def download_by_token(request):
    """
    /download?token=<token>
    -----------------------
    Уязвимость образовательная: простой предсказуемый токен-стор (в реальном проекте это может быть
    запись в БД со случайным длинным токеном). Здесь — демонстрация того, что короткие/предсказуемые
    токены легко перебираются.

    Здесь реализован крайне упрощённый маппинг токен -> файл. В реальном приложении
    используйте криптографически стойкие токены и храните их в БД с правами/expiry.
    """
    token = request.GET.get("token", "")
    token = unquote(token or "")
    # В учебной демо-ветке — предсказуемые токены (не делай так в проде)
    # Демонстрационный словарь (имитирует «секретный» URL)
    SIMPLE_TOKEN_MAP = {
        "resume_1": "resumes/1/sample.txt",  # демонстрация: предсказуемый token -> путь
        "backup": "backups/db_dump.sql",
    }
    target = SIMPLE_TOKEN_MAP.get(token)
    if not target:
        raise Http404("Not found")

    # Формируем реальный путь в MEDIA_ROOT; убедимся, что не делаем path traversal
    media_root = getattr(settings, "MEDIA_ROOT", None)
    if not media_root:
        raise Http404("Server misconfigured")

    full = os.path.normpath(os.path.join(media_root, target))
    if not full.startswith(os.path.normpath(media_root)):
        # защитный чек — но основной дизайн токена всё ещё плох
        raise Http404("Invalid path")

    if not os.path.exists(full):
        raise Http404("File not found")

    return FileResponse(open(full, "rb"), as_attachment=True, filename=os.path.basename(full))


# --- Helpers (простые проверки ролей) ---
def is_hr_user(user):
    return user.is_authenticated and (getattr(user, "is_hr", False) or user.is_superuser or getattr(user, "is_admin", False))


def is_admin_user(user):
    return user.is_authenticated and (getattr(user, "is_admin", False) or user.is_superuser)


# ---------------- HR views ----------------
@login_required(login_url="hr:login")
def hr_candidates_list(request):
    """
    Список кандидатов для HR: только кандидаты, созданные текущим HR-пользователем.
    Админ также может видеть всех кандидатов (опция).
    """
    user = request.user
    if not is_hr_user(user):
        return HttpResponseForbidden("Access denied: HR only area.")

    # если админ, показать всех; иначе — только свои
    if is_admin_user(user):
        qs = Candidate.objects.all().order_by("-date_created")
    else:
        qs = Candidate.objects.filter(created_by=user).order_by("-date_created")

    return render(request, "hr/hr_candidates_list.html", {"candidates": qs})


@login_required(login_url="hr:login")
def hr_candidate_detail(request, candidate_id: int):
    """
    Детали кандидата для HR. Только владелец (created_by) или HR/admin может просматривать.
    """
    candidate = get_object_or_404(Candidate, pk=candidate_id)
    user = request.user
    # доступ только если HR/admin или владелец записи
    if not (is_admin_user(user) or is_hr_user(user) and (candidate.created_by == user or is_admin_user(user))):
        return HttpResponseForbidden("Access denied.")

    resumes = candidate.resumes.all().order_by("-uploaded_at")
    return render(request, "hr/hr_candidate_detail.html", {"candidate": candidate, "resumes": resumes})


# --------------- Admin view ----------------
@login_required(login_url="hr:login")
def admin_dashboard(request):
    """
    Простая админ-доска — только для is_admin / superuser.
    Показывает всех кандидатов и резюме.
    """
    if not is_admin_user(request.user):
        return HttpResponseForbidden("Access denied: admin only.")

    candidates = Candidate.objects.all().order_by("-date_created")
    resumes = ResumeFile.objects.select_related("candidate", "uploaded_by").order_by("-uploaded_at")
    return render(request, "hr/admin_dashboard.html", {"candidates": candidates, "resumes": resumes})


# ------------- Protected file download -------------
@login_required(login_url="hr:login")
def download_resume_protected(request, resume_id: int):
    """
    Отдаёт файл резюме только после server-side ACL:
    - admin всегда может
    - владелец кандидата (candidate.created_by) и HR могут
    """
    resume = get_object_or_404(ResumeFile, pk=resume_id)
    user = request.user

    # используем модельный метод, если он есть
    if hasattr(resume, "is_accessible_by"):
        allowed = resume.is_accessible_by(user)
    else:
        # fallback: admin or owner or HR
        allowed = is_admin_user(user) or (resume.candidate.created_by == user) or is_hr_user(user)

    if not allowed:
        return HttpResponseForbidden("Access denied to file.")

    # отдаём файл через FileResponse (предполагаем, что file.path доступен)
    try:
        path = resume.file.path
    except Exception:
        raise Http404("File not available")

    if not os.path.exists(path):
        raise Http404("File not found")

    return FileResponse(open(path, "rb"), as_attachment=True, filename=resume.filename or os.path.basename(path))


@login_required(login_url="hr:login")
def index(request):
    """
    Главная страница:
     - если пользователь аноним — редиректит (login_required делает редирект автоматически)
     - если пользователь залогинен — показывает ссылки в зависимости от ролей
    """
    user = request.user
    ctx = {
        "is_hr": is_hr_user(user),
        "is_admin": is_admin_user(user),
        "username": user.get_username(),
    }
    return render(request, "hr/index.html", ctx)
