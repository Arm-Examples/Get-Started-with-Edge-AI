"""YOLO model loading and inference."""

import time
from ultralytics import YOLO
import streamlit as st


def load_model(model_path):
    """Load YOLO model with caching."""
    if (
        "yolo_model" not in st.session_state
        or st.session_state.get("current_model") != model_path
    ):
        with st.spinner(f"Loading model {model_path}..."):
            st.session_state.yolo_model = YOLO(model_path)
            st.session_state.current_model = model_path

    return st.session_state.yolo_model


def run_inference(model, frame, confidence):
    """
    Run YOLO inference on a frame.

    Returns:
        tuple: (annotated_frame, inference_time)
    """
    start_time = time.time()
    results = model(frame, conf=confidence, verbose=False)
    inference_time = time.time() - start_time
    annotated_frame = results[0].plot()

    return annotated_frame, inference_time
