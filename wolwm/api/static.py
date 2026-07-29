"""Server-rendered web interface."""

from __future__ import annotations

import hmac
import math
import secrets
from difflib import SequenceMatcher
from typing import Annotated, Any
from urllib.parse import urlencode

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
}

EVENT_TYPE_CLASSES = {
    types.enum.EventType.DEVICE_ADDED.value: "event-type--added",
    types.enum.EventType.DEVICE_REMOVED.value: "event-type--removed",
    types.enum.EventType.WAKE.value: "event-type--wake",
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


def _event_matches(event: types.common.Event, query: str) -> bool:
    """Approximate the former fuzzy client-side event search."""

    normalized_query = query.strip().casefold()
    if not normalized_query:
        return True

    event_type = str(event.event_type).replace("_", " ")
    searchable = f"{event_type} {event.event_data}".casefold()
    if normalized_query in searchable:
        return True

    return any(
        SequenceMatcher(None, normalized_query, word).ratio() >= 0.72
        for word in searchable.split()
    )


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


@ui.get("/ui/events", response_class=HTMLResponse, include_in_schema=False)
def events_page(
    request: Request,
    q: Annotated[str, Query(max_length=120)] = "",
    sort: Annotated[str, Query(max_length=20)] = "",
    direction: Annotated[str, Query(max_length=4)] = "asc",
    page: Annotated[int, Query(ge=1)] = 1,
    notice: Annotated[str, Query(max_length=120)] = "",
    kind: Annotated[str, Query(max_length=20)] = "success",
) -> HTMLResponse:
    """Render filtered, sorted, and paginated events."""

    events = [
        event
        for event in services.events.get_events().events
        if _event_matches(event, q)
    ]

    sort_keys = {
        "timestamp": lambda event: event.timestamp,
        "event_type": lambda event: str(event.event_type),
        "event_data": lambda event: event.event_data.casefold(),
    }
    if sort in sort_keys:
        events.sort(
            key=sort_keys[sort],
            reverse=direction == "desc",
        )
    else:
        sort = ""

    direction = "desc" if direction == "desc" else "asc"
    page_count = max(1, math.ceil(len(events) / EVENTS_PAGE_SIZE))
    current_page = min(page, page_count)
    page_start = (current_page - 1) * EVENTS_PAGE_SIZE
    visible_events = events[page_start : page_start + EVENTS_PAGE_SIZE]

    def events_url(**updates: Any) -> str:
        query = {
            "q": q,
            "sort": sort,
            "direction": direction,
            "page": current_page,
        }
        query.update(updates)
        compact_query = {
            key: value
            for key, value in query.items()
            if value not in ("", None)
        }
        return f"/ui/events?{urlencode(compact_query)}"

    context = _base_context(
        active_page="events",
        title="Events",
        notice=notice,
        kind=kind,
        initial_notice="Events loaded",
    )
    context.update(
        {
            "events": visible_events,
            "event_type_labels": EVENT_TYPE_LABELS,
            "event_type_classes": EVENT_TYPE_CLASSES,
            "query": q,
            "sort": sort,
            "direction": direction,
            "current_page": current_page,
            "page_count": page_count,
            "events_url": events_url,
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
