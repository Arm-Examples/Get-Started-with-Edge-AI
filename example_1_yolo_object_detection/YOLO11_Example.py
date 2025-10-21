"""Main entry point for YOLO11 Streamlit demo."""

import time
from collections import deque
import cv2
import streamlit as st

from modules.device_config import IS_RASPBERRY_PI
from modules.camera_handler import setup_camera, get_frame
from modules.ui_components import (
    setup_page_config,
    render_header,
    render_arm_logo,
    setup_sidebar,
    upload_video,
    display_metrics,
)
from modules.yolo_inference import load_model, run_inference


def process_video_file(
    video_path, confidence, model_path, task, stats_placeholder, result_frame
):
    """Process an uploaded video file with YOLO inference."""
    model = load_model(model_path)
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        stats_placeholder.error("Could not open video file.")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps_video = cap.get(cv2.CAP_PROP_FPS)

    stats_placeholder.info(
        f"📹 Processing {total_frames} frames at {fps_video:.1f} FPS..."
    )

    progress_bar = st.progress(0)
    frame_count = 0
    inference_times = []

    try:
        while True:
            success, frame = cap.read()

            if not success or frame is None:
                break

            annotated_frame, inference_time = run_inference(model, frame, confidence)
            inference_times.append(inference_time)

            if frame_count % 5 == 0:
                # Center the video frame
                with result_frame.container():
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.image(
                            annotated_frame,
                            channels="BGR",
                            caption=f"{task} - Frame {frame_count}/{total_frames}",
                            width="stretch",
                        )

                avg_inference_time = sum(inference_times) / len(inference_times)
                inference_fps = (
                    1.0 / avg_inference_time if avg_inference_time > 0 else 0
                )

                stats_placeholder.markdown(f"""
                **Progress:** {frame_count}/{total_frames} frames  
                **Avg Inference Time:** {avg_inference_time * 1000:.1f} ms  
                **Inference FPS:** {inference_fps:.1f}
                """)

                progress_bar.progress(frame_count / total_frames)

            frame_count += 1

        progress_bar.progress(1.0)
        avg_inference_time = sum(inference_times) / len(inference_times)
        inference_fps = 1.0 / avg_inference_time if avg_inference_time > 0 else 0

        stats_placeholder.success(f"""
        ✅ **Processing Complete!**  
        - Processed {frame_count} frames  
        - Average inference time: {avg_inference_time * 1000:.1f} ms  
        - Inference FPS: {inference_fps:.1f}
        """)

    finally:
        cap.release()


def run_camera_stream(
    camera_thread,
    cap,
    use_picamera,
    model,
    task,
    yolo_enabled,
    confidence,
    stats_placeholder,
    result_frame,
    source,
):
    """Run the continuous camera stream with optional YOLO inference."""
    frame_times = deque(maxlen=30)
    inference_times = deque(maxlen=30)

    try:
        while True:
            frame_start = time.time()

            # Capture frame
            success, frame, error = get_frame(camera_thread, cap, use_picamera)

            if error:
                st.error(f"Camera error: {error}")
                break

            if not success or frame is None:
                st.warning("No more frames.")
                break

            # Run YOLO inference if enabled
            if yolo_enabled and model is not None:
                annotated_frame, inference_time = run_inference(
                    model, frame, confidence
                )
                inference_times.append(inference_time)
            else:
                annotated_frame = frame

            # Calculate FPS
            frame_times.append(frame_start)

            overall_fps = 0.0
            inference_fps = 0.0
            avg_inference_time = 0.0

            if len(frame_times) >= 2:
                time_diff = frame_times[-1] - frame_times[0]
                if time_diff > 0:
                    overall_fps = (len(frame_times) - 1) / time_diff

            if len(inference_times) > 0:
                avg_inference_time = sum(inference_times) / len(inference_times)
                if avg_inference_time > 0:
                    inference_fps = 1.0 / avg_inference_time

            caption = f"{task} Result" if yolo_enabled else "Camera Feed"

            # Center the video feed using columns
            with result_frame.container():
                col1, col2, col3 = st.columns([1, 5, 1])
                with col2:
                    st.image(
                        annotated_frame,
                        channels="BGR",
                        caption=caption,
                        width="stretch",
                    )

            # Display metrics below the feed
            with stats_placeholder.container():
                display_metrics(
                    overall_fps, inference_fps, avg_inference_time, yolo_enabled, source
                )

    finally:
        pass  # Camera cleanup handled by session state


def run_detection(source, confidence, model_path, task, yolo_enabled):
    """Run detection/segmentation/pose estimation on the selected source."""

    # Create display placeholders
    result_frame = st.empty()
    stats_placeholder = st.empty()

    # Determine video source and camera type
    use_picamera = source == "picamera" and IS_RASPBERRY_PI

    # Handle video file source
    if source == "video":
        video_path, process_button = upload_video()

        if video_path is None:
            stats_placeholder.info("📁 Please upload a video file to continue.")
            return

        stats_placeholder.success("✅ Video uploaded successfully!")

        if not process_button:
            result_frame.info("👆 Click 'Process Video with YOLO' to start analysis.")
            return

        # Clear placeholders before processing
        stats_placeholder.empty()
        result_frame.empty()

        process_video_file(
            video_path, confidence, model_path, task, stats_placeholder, result_frame
        )
        return

    # Camera source handling
    if use_picamera:
        video_source = None
    elif source in ["webcam", "picamera"]:
        video_source = 0
    else:
        stats_placeholder.info("Please select a video source.")
        return

    # Load model if YOLO is enabled
    model = None
    if yolo_enabled:
        model = load_model(model_path)
        st.sidebar.success(f"✅ Model loaded: {task}")

    # Setup camera
    camera_thread, cap = setup_camera(video_source, use_picamera)

    if camera_thread is None and cap is None:
        return  # Error already displayed

    # Run camera stream
    run_camera_stream(
        camera_thread,
        cap,
        use_picamera,
        model,
        task,
        yolo_enabled,
        confidence,
        stats_placeholder,
        result_frame,
        source,
    )


def main():
    """Main application function."""
    setup_page_config()

    render_arm_logo()

    render_header()

    source, confidence, model_path, task, yolo_enabled = setup_sidebar()

    run_detection(source, confidence, model_path, task, yolo_enabled)


if __name__ == "__main__":
    main()
