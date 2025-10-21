"""Device configuration and platform detection."""

import logging

# Suppress Streamlit warnings
logging.getLogger("streamlit.runtime.media_file_storage").setLevel(logging.CRITICAL)
logging.getLogger("streamlit.web.server.media_file_handler").setLevel(logging.CRITICAL)

# Detect if running on Raspberry Pi
IS_RASPBERRY_PI = False
try:
    with open("/proc/device-tree/model", "r") as f:
        if "Raspberry Pi" in f.read():
            IS_RASPBERRY_PI = True
except (FileNotFoundError, OSError, PermissionError):
    IS_RASPBERRY_PI = False

# Camera configuration
CAMERA_CONFIG = {
    "pi_camera": {"format": "BGR888", "size": (800, 600), "warmup_time": 2.0},
    "webcam": {"source": 0, "width": 800, "height": 600},
}


def get_source_options():
    """Get available video source options based on platform."""
    if IS_RASPBERRY_PI:
        return ["picamera", "video"]
    else:
        return ["webcam", "video"]


def get_platform_info():
    """Get platform display string."""
    return (
        "🥧 Raspberry Pi (Pi Camera)" if IS_RASPBERRY_PI else "💻 Desktop/Mac (Webcam)"
    )
