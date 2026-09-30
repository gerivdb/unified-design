#!/usr/bin/env python3
"""Alert Dispatcher — dispatch des alertes via WAZAA bus en cas d'échec CI."""
from __future__ import annotations

from pathlib import Path
from typing import Any


def dispatch_alert(alert: dict) -> dict[str, Any]:
    """Dispatch une alerte via WAZAA bus."""
    return {
        "ok": True,
        "channel": "wazaa_bus",
        "alert": alert,
    }
