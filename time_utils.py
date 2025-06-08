from datetime import timedelta


def seconds_to_hms(seconds):
    """Convert seconds to HH:MM:SS format."""
    return str(timedelta(seconds=float(seconds))).split(".")[0]


def format_time(seconds, include_ms=True, include_tenths=False):
    """Format seconds as H:M:S with optional milliseconds or tenths."""
    if seconds is None or seconds < 0:
        if include_ms:
            return "--:--:--.-" if include_tenths else "--:--:--.---"
        return "--:--:--"

    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)

    if include_ms:
        if include_tenths:
            tenths = int((seconds - int(seconds)) * 10)
            return f"{h}:{m:02}:{s:02}.{tenths}"
        ms = int(round((seconds - int(seconds)) * 1000))
        return f"{h}:{m:02}:{s:02}.{ms:03}"
    return f"{h}:{m:02}:{s:02}"


def compute_scroll_speed(T_loop, T_zoom, canvas_width):
    """Return scroll speed (px/s) for static elements during dynamic zoom."""
    if T_loop <= 0 or T_zoom <= 0 or canvas_width <= 0:
        return 0.0
    v_frac = (T_loop - 0.9 * T_zoom) / (T_loop * T_zoom)
    return v_frac * canvas_width

