"""Server-rendered web interface."""

from __future__ import annotations

import hmac
import secrets
from datetime import UTC, datetime
from typing import Annotated, Any
from urllib.parse import urlencode
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Form, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from wolwm import services, types
from wolwm.config.definitions import MAIN_DIR
from wolwm.log import logger

ui = APIRouter()

UI_DIR = MAIN_DIR / "ui"
UI_STATIC_DIR = UI_DIR / "static"
templates = Jinja2Templates(directory=str(UI_DIR / "templates"))

CSRF_COOKIE = "wolwm_csrf"
EVENTS_PAGE_SIZE = 10
NOTICE_KINDS = {"success", "error"}

EVENT_TYPE_LABELS = {
    types.enum.EventType.DEVICE_ADDED.value: "DEVICE ADDED",
    types.enum.EventType.DEVICE_REMOVED.value: "DEVICE REMOVED",
    types.enum.EventType.WAKE.value: "WAKE REQUEST",
    types.enum.EventType.SCHEDULED_WAKE.value: "SCHEDULED WAKE",
    types.enum.EventType.SCHEDULED_WAKE_FAILED.value: "SCHEDULE FAILED",
    types.enum.EventType.SCHEDULE_CREATED.value: "SCHEDULE ADDED",
    types.enum.EventType.SCHEDULE_REMOVED.value: "SCHEDULE REMOVED",
}

EVENT_TYPE_CLASSES = {
    types.enum.EventType.DEVICE_ADDED.value: "event-type--added",
    types.enum.EventType.DEVICE_REMOVED.value: "event-type--removed",
    types.enum.EventType.WAKE.value: "event-type--wake",
    types.enum.EventType.SCHEDULED_WAKE.value: "event-type--scheduled",
    types.enum.EventType.SCHEDULED_WAKE_FAILED.value: "event-type--failed",
    types.enum.EventType.SCHEDULE_CREATED.value: "event-type--added",
    types.enum.EventType.SCHEDULE_REMOVED.value: "event-type--removed",
}

SCHEDULE_FREQUENCY_LABELS = {
    types.enum.ScheduleFrequency.ONCE.value: "Once",
    types.enum.ScheduleFrequency.DAILY.value: "Daily",
    types.enum.ScheduleFrequency.WEEKDAYS.value: "Weekdays",
    types.enum.ScheduleFrequency.WEEKLY.value: "Weekly",
}


def _render(
    request: Request,
    template_name: str,
    context: dict[str, Any],
    *,
    status_code: int = 200,
) -> HTMLResponse:
    """Render a UI page and ensure it has a same-site CSRF token."""

    csrf_token = request.cookies.get(CSRF_COOKIE)
    set_csrf_cookie = csrf_token is None
    if csrf_token is None:
        csrf_token = secrets.token_urlsafe(32)

    page_context = {
        "request": request,
        "csrf_token": csrf_token,
        **context,
    }
    response = templates.TemplateResponse(
        request=request,
        name=template_name,
        context=page_context,
        status_code=status_code,
    )
    if set_csrf_cookie:
        response.set_cookie(
            CSRF_COOKIE,
            csrf_token,
            httponly=True,
            samesite="strict",
        )
    return response


def _valid_csrf(request: Request, csrf_token: str) -> bool:
    """Validate a form token without maintaining server-side session state."""

    cookie_token = request.cookies.get(CSRF_COOKIE, "")
    return bool(cookie_token) and hmac.compare_digest(cookie_token, csrf_token)


def _redirect_with_notice(
    location: str,
    notice: str,
    kind: str = "success",
) -> RedirectResponse:
    """Redirect after a form submission and carry a short notification."""

    separator = "&" if "?" in location else "?"
    query = urlencode({"notice": notice, "kind": kind})
    return RedirectResponse(f"{location}{separator}{query}", status_code=303)


def _base_context(
    *,
    active_page: str | None,
    title: str,
    notice: str,
    kind: str,
    initial_notice: str,
) -> dict[str, Any]:
    safe_kind = kind if kind in NOTICE_KINDS else "success"
    return {
        "active_page": active_page,
        "title": title,
        "notice": notice or initial_notice,
        "notice_kind": safe_kind,
    }


@ui.get("/", include_in_schema=False)
def default_redirect() -> RedirectResponse:
    """Redirect the application root to the web interface."""

    return RedirectResponse(url="/ui/", status_code=307)


@ui.get("/ui", include_in_schema=False)
def ui_redirect() -> RedirectResponse:
    """Keep the canonical UI URL trailing slash."""

    return RedirectResponse(url="/ui/", status_code=307)


@ui.get("/ui/", response_class=HTMLResponse, include_in_schema=False)
def devices_page(
    request: Request,
    notice: Annotated[str, Query(max_length=120)] = "",
    kind: Annotated[str, Query(max_length=20)] = "success",
) -> HTMLResponse:
    """Render the devices page."""

    devices = services.devices.get_devices().devices
    context = _base_context(
        active_page="devices",
        title="Devices",
        notice=notice,
        kind=kind,
        initial_notice="Devices loaded",
    )
    context["devices"] = devices
    return _render(request, "devices.html", context)


@ui.post("/ui/devices", include_in_schema=False)
def add_device(
    request: Request,
    csrf_token: Annotated[str, Form()],
    name: Annotated[str, Form(max_length=100)],
    mac: Annotated[str, Form(max_length=17)],
) -> RedirectResponse:
    """Add a device from the server-rendered form."""

    if not _valid_csrf(request, csrf_token):
        return _redirect_with_notice("/ui/", "Invalid request token", "error")

    normalized_name = name.strip()
    normalized_mac = mac.strip()
    if not normalized_name:
        return _redirect_with_notice("/ui/", "Unable to add device", "error")

    try:
        services.devices.add_device(
            types.api.AddDeviceReq(name=normalized_name, mac=normalized_mac)
        )
    except Exception as err:
        logger.error(f"Error while adding device from the web interface: {err}")
        return _redirect_with_notice("/ui/", "Unable to add device", "error")

    return _redirect_with_notice("/ui/", "Device added")


@ui.post("/ui/devices/{device_id}/wake", include_in_schema=False)
def wake_device(
    device_id: str,
    request: Request,
    csrf_token: Annotated[str, Form()],
) -> RedirectResponse:
    """Send a magic packet from the server-rendered interface."""

    if not _valid_csrf(request, csrf_token):
        return _redirect_with_notice("/ui/", "Invalid request token", "error")

    try:
        services.wake.wake_device(types.api.WakeReq(device_id=device_id))
    except Exception as err:
        logger.error(f"Error while waking device from the web interface: {err}")
        return _redirect_with_notice("/ui/", "Unable to wake device", "error")

    return _redirect_with_notice("/ui/", "Magic Packet correctly sent")


@ui.post("/ui/devices/{device_id}/delete", include_in_schema=False)
def delete_device(
    device_id: str,
    request: Request,
    csrf_token: Annotated[str, Form()],
) -> RedirectResponse:
    """Delete a device from the server-rendered interface."""

    if not _valid_csrf(request, csrf_token):
        return _redirect_with_notice("/ui/", "Invalid request token", "error")

    try:
        services.devices.delete_device(device_id)
    except Exception as err:
        logger.error(f"Error while deleting device from the web interface: {err}")
        return _redirect_with_notice("/ui/", "Unable to remove device", "error")

    return _redirect_with_notice("/ui/", "Device removed")


def _local_schedule_time(schedule: types.common.WakeSchedule) -> str:
    """Format a schedule's UTC timestamp in its chosen time zone."""

    if schedule.next_run_at is None:
        return "—"
    local_time = schedule.next_run_at.replace(tzinfo=UTC).astimezone(
        ZoneInfo(schedule.timezone)
    )
    return local_time.strftime("%Y-%m-%d %H:%M")


@ui.get("/ui/schedules", response_class=HTMLResponse, include_in_schema=False)
def schedules_page(
    request: Request,
    notice: Annotated[str, Query(max_length=120)] = "",
    kind: Annotated[str, Query(max_length=20)] = "success",
) -> HTMLResponse:
    """Render persistent scheduled wake-ups."""

    devices = services.devices.get_devices().devices
    app_timezone = services.schedules.configured_timezone()
    devices_by_id = {device.id: device for device in devices}
    schedule_rows = [
        {
            "schedule": schedule,
            "device": devices_by_id.get(schedule.device_id),
            "next_run": _local_schedule_time(schedule),
        }
        for schedule in services.schedules.get_schedules().schedules
    ]

    context = _base_context(
        active_page="schedules",
        title="Schedules",
        notice=notice,
        kind=kind,
        initial_notice="Schedules loaded",
    )
    context.update(
        {
            "devices": devices,
            "schedule_rows": schedule_rows,
            "frequency_labels": SCHEDULE_FREQUENCY_LABELS,
            "app_timezone": app_timezone,
        }
    )
    return _render(request, "schedules.html", context)


@ui.post("/ui/schedules", include_in_schema=False)
def add_schedule(
    request: Request,
    csrf_token: Annotated[str, Form()],
    device_id: Annotated[str, Form(max_length=36)],
    scheduled_for: Annotated[str, Form(max_length=40)],
    frequency: Annotated[str, Form(max_length=20)],
    timezone: Annotated[str, Form(max_length=64)],
) -> RedirectResponse:
    """Add a scheduled wake-up from the server-rendered form."""

    if not _valid_csrf(request, csrf_token):
        return _redirect_with_notice(
            "/ui/schedules",
            "Invalid request token",
            "error",
        )

    try:
        services.schedules.create_schedule(
            types.api.CreateWakeScheduleReq(
                device_id=device_id,
                scheduled_for=datetime.fromisoformat(scheduled_for),
                frequency=types.enum.ScheduleFrequency(frequency),
                timezone=timezone,
            )
        )
    except Exception as err:
        logger.error(
            f"Error while adding schedule from the web interface: {err}"
        )
        return _redirect_with_notice(
            "/ui/schedules",
            "Unable to add schedule",
            "error",
        )

    return _redirect_with_notice("/ui/schedules", "Wake-up scheduled")


@ui.post(
    "/ui/schedules/{schedule_id}/delete",
    include_in_schema=False,
)
def delete_schedule(
    schedule_id: str,
    request: Request,
    csrf_token: Annotated[str, Form()],
) -> RedirectResponse:
    """Delete a wake-up schedule from the server-rendered interface."""

    if not _valid_csrf(request, csrf_token):
        return _redirect_with_notice(
            "/ui/schedules",
            "Invalid request token",
            "error",
        )

    try:
        services.schedules.delete_schedule(schedule_id)
    except Exception as err:
        logger.error(
            f"Error while deleting schedule from the web interface: {err}"
        )
        return _redirect_with_notice(
            "/ui/schedules",
            "Unable to remove schedule",
            "error",
        )

    return _redirect_with_notice("/ui/schedules", "Schedule removed")


@ui.get("/ui/events", response_class=HTMLResponse, include_in_schema=False)
def events_page(
    request: Request,
    notice: Annotated[str, Query(max_length=120)] = "",
    kind: Annotated[str, Query(max_length=20)] = "success",
) -> HTMLResponse:
    """Render all events for client-side search, sorting, and pagination."""

    events = services.events.get_events().events

    context = _base_context(
        active_page="events",
        title="Events",
        notice=notice,
        kind=kind,
        initial_notice="Events loaded",
    )
    context.update(
        {
            "events": events,
            "event_type_labels": EVENT_TYPE_LABELS,
            "event_type_classes": EVENT_TYPE_CLASSES,
            "events_page_size": EVENTS_PAGE_SIZE,
        }
    )
    return _render(request, "events.html", context)


@ui.get("/ui/{rest_of_path:path}", response_class=HTMLResponse, include_in_schema=False)
def not_found(request: Request, rest_of_path: str) -> HTMLResponse:
    """Render the UI's not-found page."""

    del rest_of_path
    context = _base_context(
        active_page=None,
        title="Page not found",
        notice="",
        kind="success",
        initial_notice="",
    )
    return _render(request, "404.html", context, status_code=404)
