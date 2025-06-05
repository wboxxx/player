import subprocess
from typing import List, Optional


def extract_keyframes(
    video_path: str,
    start_time_sec: Optional[float] = None,
    duration_sec: Optional[float] = None,
    end_time_sec: Optional[float] = None,
) -> List[float]:
    """Extract keyframe timestamps from a video using ffprobe."""
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "frame=pkt_pts_time,pict_type",
        "-of",
        "csv=p=0",
        video_path,
    ]
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.PIPE).decode()
    except Exception:
        return []
    keyframes = []
    for line in output.strip().splitlines():
        try:
            time_str, frame_type = line.split(",")
        except ValueError:
            continue
        if frame_type.strip() == "I":
            try:
                t = float(time_str)
            except ValueError:
                continue
            keyframes.append(t)

    if start_time_sec is not None:
        end = start_time_sec + duration_sec if duration_sec is not None else end_time_sec
        if end is not None:
            keyframes = [t for t in keyframes if start_time_sec <= t < end]
        else:
            keyframes = [t for t in keyframes if t >= start_time_sec]

    return keyframes
