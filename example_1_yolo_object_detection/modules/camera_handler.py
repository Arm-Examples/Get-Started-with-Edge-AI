"""Camera handling for Pi Camera and Webcam."""

import time
import threading
from queue import Queue, Empty
import cv2
import streamlit as st
from modules.device_config import IS_RASPBERRY_PI, CAMERA_CONFIG

if IS_RASPBERRY_PI:
    from picamera2 import Picamera2


class PiCameraThread(threading.Thread):
    """Thread-safe wrapper for Picamera2 to avoid cleanup issues."""

    def __init__(self):
        super().__init__(daemon=True)
        self.frame_queue = Queue(maxsize=2)
        self.stop_event = threading.Event()
        self.camera = None
        self.error = None

    def run(self):
        """Run the camera capture loop in a separate thread."""
        try:
            config_settings = CAMERA_CONFIG["pi_camera"]
            self.camera = Picamera2()
            config = self.camera.create_preview_configuration(
                main={
                    "format": config_settings["format"],
                    "size": config_settings["size"],
                }
            )
            self.camera.configure(config)
            self.camera.start()
            self.camera.set_controls({"AwbEnable": True, "AeEnable": True})
            time.sleep(config_settings["warmup_time"])

            while not self.stop_event.is_set():
                try:
                    frame = self.camera.capture_array()
                    try:
                        self.frame_queue.put(frame, block=False)
                    except Exception:
                        pass  # Queue full, skip frame
                except Exception as e:
                    if not self.stop_event.is_set():
                        self.error = str(e)
                    break

        except Exception as e:
            self.error = str(e)
        finally:
            if self.camera:
                try:
                    self.camera.stop()
                    time.sleep(0.3)
                    self.camera.close()
                except Exception:
                    pass

    def get_frame(self, timeout=0.5):
        """Get the latest frame from the queue."""
        try:
            return self.frame_queue.get(timeout=timeout)
        except Empty:
            return None

    def stop(self):
        """Signal the thread to stop."""
        self.stop_event.set()


def initialize_camera(source, use_picamera):
    """Initialize camera based on source type."""
    if use_picamera:
        camera_thread = PiCameraThread()
        camera_thread.start()
        time.sleep(2.5)

        if camera_thread.error:
            st.error(f"Could not initialize Pi Camera: {camera_thread.error}")
            camera_thread.stop()
            return None, None

        return camera_thread, None
    else:
        # Use OpenCV VideoCapture for webcam/video
        cap = cv2.VideoCapture(source)

        if not cap.isOpened():
            st.error(f"Could not open video source: {source}")
            return None, None

        return None, cap


def get_frame(camera_thread, cap, use_picamera):
    """Get frame from camera (abstracts Pi Camera vs Webcam)."""
    if use_picamera:
        frame = camera_thread.get_frame(timeout=1.0)
        success = frame is not None
        error = camera_thread.error if camera_thread else None
        return success, frame, error
    else:
        success, frame = cap.read()
        return success, frame, None


def cleanup_camera(camera_thread, cap):
    """Clean up camera resources."""
    if camera_thread:
        camera_thread.stop()
        camera_thread.join(timeout=3.0)
    if cap:
        cap.release()


def setup_camera(video_source, use_picamera):
    """Get camera from session state or initialize if needed."""
    # Initialize session state for camera
    if "camera_initialized" not in st.session_state:
        st.session_state.camera_initialized = False
        st.session_state.camera_thread = None
        st.session_state.cap = None
        st.session_state.use_picamera = None

    # Initialize camera (only once or when source changes)
    if (
        not st.session_state.camera_initialized
        or st.session_state.use_picamera != use_picamera
    ):
        if st.session_state.camera_initialized:
            cleanup_camera(st.session_state.camera_thread, st.session_state.cap)

        camera_thread, cap = initialize_camera(video_source, use_picamera)

        if camera_thread is None and cap is None:
            return None, None  # Error already displayed

        st.session_state.camera_thread = camera_thread
        st.session_state.cap = cap
        st.session_state.camera_initialized = True
        st.session_state.use_picamera = use_picamera

    return st.session_state.camera_thread, st.session_state.cap
