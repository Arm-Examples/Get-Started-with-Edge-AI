"""Reusable Streamlit UI components."""

import io
import streamlit as st
from modules.device_config import get_source_options, get_platform_info


def setup_page_config():
    """Set up page configuration (must be called first)."""
    st.set_page_config(
        page_title="YOLO11 Edge AI Demo",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def render_header():
    """Render the main page header."""
    st.markdown(
        """<h2 style="color:#58D3F7; text-align:center; 
        font-family: 'Archivo', sans-serif; margin-bottom: 10px;">🤖 Object Detection using Ultralytics YOLO11</h2>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """<p style="color:#B8B8B8; text-align:center; font-family: 'Archivo', sans-serif; font-size:15px; margin-top: 5px; margin-bottom: 5px;">
        Real-time object detection demonstrating Edge AI concepts: model size trade-offs, 
        performance constraints, and local inference.</p>""",
        unsafe_allow_html=True,
    )

    platform_info = get_platform_info()
    st.markdown(
        f"""<p style="color:#B8B8B8; text-align:center; font-family: 'Archivo', sans-serif; font-size:15px; margin-top: 5px;">
        Running on: {platform_info}</p>""",
        unsafe_allow_html=True,
    )


def render_arm_logo():
    """Render Arm logo at top of sidebar."""
    # Center the image using columns
    col1, col2, col3 = st.sidebar.columns([1, 2, 1])
    with col2:
        st.image("images/arm-logo-white-rgb.svg", width=150)
    
    st.sidebar.markdown(
        """
        <p style="font-size: 12px; color: #888; margin-top: 8px; text-align: center;">
            <a href="https://developer.arm.com/edge-ai" target="_blank" style="color: #58D3F7; text-decoration: none;">
                Learn more about Edge AI at arm
            </a>
        </p>
        """,
        unsafe_allow_html=True,
    )

    # Add Ultralytics logo below Arm logo
    st.sidebar.markdown(
        """
        <div style="text-align: center; margin-bottom: 20px;">
            <p style="font-size: 11px; color: #888; margin-bottom: 8px;">
                Powered by <a href="https://docs.ultralytics.com/" target="_blank" style="color: #58D3F7; text-decoration: none;">Ultralytics YOLO</a>
            </p>
            <a href="https://docs.ultralytics.com/" target="_blank">
                <img src="https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Original.svg" width="150">
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_detectable_objects_banner(yolo_enabled, task):
    """Render subtle banner showing common detectable objects above metrics."""
    if yolo_enabled:
        # Match video feed layout: [1, 2, 1] with banner filling the center column
        left_pad, center_col, right_pad = st.columns([1, 2, 1])
        
        with center_col:
            if task == "Pose Estimation":
                st.markdown(
                    """
                    <div style='background-color: #2a2a2a; 
                                padding: 8px 15px; 
                                border-radius: 6px; 
                                border-left: 3px solid #f59e0b;
                                margin-bottom: 15px;
                                text-align: center;'>
                        <p style='color: #fbbf24; margin: 0; font-size: 12px;'>
                            ℹ️ Pose estimation detects people and tracks body keypoints
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    """
                    <div style='background-color: #2a2a2a; 
                                padding: 8px 15px; 
                                border-radius: 6px; 
                                border-left: 3px solid #58D3F7;
                                margin-bottom: 15px;
                                text-align: center;'>
                        <p style='color: #B8B8B8; 
                                  margin: 0; 
                                  font-size: 12px; 
                                  line-height: 1.5;'>
                            🎯 Detects: 👤 People • 🚗 Vehicles • 🐕 Animals • 🪑 Furniture • 📱 Electronics • 🎒 Accessories
                        </p>
                        <p style='color: #888; 
                                  margin: 4px 0 0 0; 
                                  font-size: 11px;'>
                            <a href="https://github.com/ultralytics/ultralytics/blob/main/ultralytics/cfg/datasets/coco.yaml" 
                               target="_blank" 
                               style="color: #58D3F7; text-decoration: none;">
                                See full list of 80 objects →
                            </a>
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def get_model_options(task):
    """Get available models for a given task."""
    models = {
        "Detection": ["yolo11n.pt", "yolo11s.pt", "yolo11m.pt"],
        "Segmentation": ["yolo11n-seg.pt", "yolo11s-seg.pt", "yolo11m-seg.pt"],
        "Pose Estimation": ["yolo11n-pose.pt", "yolo11s-pose.pt", "yolo11m-pose.pt"],
    }
    return models.get(task, models["Detection"])


def setup_sidebar():
    """Configure sidebar with all settings."""
    # Add spacing above YOLO toggle
    st.sidebar.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

    # Prominent instruction box above the checkbox
    st.sidebar.markdown(
        """
        <div style='background: linear-gradient(135deg, #1e3a5f 0%, #2d5a8a 100%); 
                    padding: 15px; 
                    border-radius: 10px; 
                    border: 2px solid #58D3F7;
                    margin-bottom: 10px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                    text-align: center;'>
            <p style='color: #58D3F7; 
                      font-size: 14px; 
                      font-weight: bold; 
                      margin: 0;
                      text-transform: uppercase;
                      letter-spacing: 1px;'>
                👇Enable/Disable YOLO
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # YOLO toggle at the top (will be used for non-video sources)
    yolo_enabled = st.sidebar.checkbox(
        "🎯 Enable YOLO Detection",
        value=False,
        key="yolo_checkbox",
        help="Enable real-time YOLO object detection on the camera feed",
    )

    # Compact separator with reduced margins
    st.sidebar.markdown(
        "<hr style='margin-top: 15px; margin-bottom: 10px;'>", unsafe_allow_html=True
    )

    st.sidebar.title("Settings")

    # Task selection
    task = st.sidebar.selectbox(
        "Task", ("Detection", "Segmentation", "Pose Estimation")
    )

    # Source selection
    source_options = get_source_options()
    source = st.sidebar.selectbox("Source", source_options)

    # Confidence threshold
    confidence = st.sidebar.slider("Confidence", 0.0, 1.0, 0.55, 0.05)

    # Model selection
    models = get_model_options(task)
    selected_model = st.sidebar.selectbox("Model", models, index=2)

    return source, confidence, selected_model, task, yolo_enabled


def render_yolo_toggle(source):
    """Render YOLO toggle checkbox on main page (centered)."""
    if source != "video":
        # Use columns for checkbox centering with more space for the checkbox
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            yolo_enabled = st.checkbox(
                "🎯 Enable YOLO Detection", value=False, key="yolo_checkbox"
            )
        return yolo_enabled
    else:
        return False  # Video will be processed on demand


def upload_video():
    """Handle video file upload with process button."""
    vid_file = st.sidebar.file_uploader(
        "Upload Video File", type=["mp4", "avi", "mov", "mkv"]
    )

    if vid_file is not None:
        video_bytes = io.BytesIO(vid_file.read())
        with open("temp_video.mp4", "wb") as out:
            out.write(video_bytes.read())

        # Add button to process video
        process_video = st.sidebar.button(
            "▶️ Process Video with YOLO", use_container_width=True
        )

        return "temp_video.mp4", process_video

    return None, False


def display_metrics(
    overall_fps, inference_fps, avg_inference_time, yolo_enabled, source, task
):
    """Display performance metrics with detectable objects banner above."""
    # Show detectable objects banner above metrics
    render_detectable_objects_banner(yolo_enabled, task)
    
    st.markdown(
        "<h4 style='text-align: center;'>⚡ Performance Metrics</h4>",
        unsafe_allow_html=True,
    )

    # Match video feed layout: [1, 2, 1] with metrics filling the center column
    left_pad, center_col, right_pad = st.columns([1, 2, 1])

    with center_col:
        # Create 3 equal columns for metrics within the centered area
        col1, col2, col3 = st.columns(3, gap="medium")

        with col1:
            st.metric(
                label="Overall FPS",
                value=f"{overall_fps:.1f}",
                help="Frames per second including camera capture, YOLO inference, and Streamlit UI rendering. Lower than YOLO FPS due to UI overhead."
                if yolo_enabled
                else "Camera feed frames per second including capture and Streamlit UI rendering (without YOLO inference).",
            )

        with col2:
            if yolo_enabled:
                st.metric(
                    label="YOLO FPS",
                    value=f"{inference_fps:.1f}",
                    help="Pure YOLO model inference speed - how many frames per second the model can process. This represents the raw AI performance.",
                )
            else:
                st.metric(
                    label="YOLO FPS",
                    value="N/A",
                    help="Enable YOLO Detection to see inference speed metrics.",
                )

        with col3:
            if yolo_enabled:
                st.metric(
                    label="Inference Time",
                    value=f"{avg_inference_time * 1000:.0f} ms",
                    help="Average time in milliseconds for the YOLO model to process one frame.",
                )
            else:
                st.metric(
                    label="Inference Time",
                    value="N/A",
                    help="Enable YOLO Detection to see inference time metrics.",
                )
