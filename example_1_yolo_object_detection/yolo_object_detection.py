import cv2
import time
import psutil
import argparse
from ultralytics import YOLO


def get_memory_usage():
    return psutil.Process().memory_info().rss / (1024 * 1024)


def parse_arguments():
    parser = argparse.ArgumentParser(description="YOLOv8 object detection with webcam")
    parser.add_argument(
        "--model",
        type=str,
        default="nano",
        help="YOLOv8 model size (nano, small, medium, large)",
    )
    return parser.parse_args()


def get_model_filename(model_name):
    model_map = {
        "nano": "yolov8n.pt",
        "small": "yolov8s.pt",
        "medium": "yolov8m.pt",
        "large": "yolov8l.pt",
    }

    if model_name in model_map:
        return model_map[model_name]
    else:
        return model_name


def load_yolo_model(model_file, model_name):
    print(f"Loading {model_name} model: {model_file}")
    try:
        model = YOLO(model_file)
        print("Model loaded successfully")
        return model
    except Exception as e:
        print(f"Failed to load model: {e}")
        raise


def initialize_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam.")

    print("Webcam opened. Press 'q' to quit.")
    return cap


def run_inference(model, frame):
    start_time = time.time()
    results = model(frame, verbose=False)
    end_time = time.time()

    inference_time = end_time - start_time
    fps = 1.0 / inference_time if inference_time > 0 else 0

    return results, inference_time, fps


def draw_detections(frame, results, class_names):
    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = class_names[cls_id]
            conf = float(box.conf[0])

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"{label} {conf:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
            )

    return frame


def add_performance_overlay(frame, inference_time, fps, memory_usage, model_name):
    stats_text = f"Model: {model_name} | Inference: {inference_time * 1000:.1f}ms | FPS: {fps:.1f} | RAM: {memory_usage:.1f} MB"

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.5
    thickness = 2
    (text_width, text_height), baseline = cv2.getTextSize(
        stats_text, font, font_scale, thickness
    )

    overlay = frame.copy()
    cv2.rectangle(overlay, (5, 5), (text_width + 20, text_height + 20), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

    text_x, text_y = 15, text_height + 15

    cv2.putText(
        frame,
        stats_text,
        (text_x - 1, text_y - 1),
        font,
        font_scale,
        (0, 0, 0),
        thickness + 1,
    )
    cv2.putText(
        frame,
        stats_text,
        (text_x + 1, text_y + 1),
        font,
        font_scale,
        (0, 0, 0),
        thickness + 1,
    )
    cv2.putText(
        frame,
        stats_text,
        (text_x - 1, text_y + 1),
        font,
        font_scale,
        (0, 0, 0),
        thickness + 1,
    )
    cv2.putText(
        frame,
        stats_text,
        (text_x + 1, text_y - 1),
        font,
        font_scale,
        (0, 0, 0),
        thickness + 1,
    )

    cv2.putText(
        frame,
        stats_text,
        (text_x, text_y),
        font,
        font_scale,
        (255, 255, 255),
        thickness,
    )
    return frame


def process_video_stream(model, cap, model_name):
    class_names = model.names

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            results, inference_time, fps = run_inference(model, frame)
            memory_usage = get_memory_usage()
            frame = draw_detections(frame, results, class_names)
            frame = add_performance_overlay(
                frame, inference_time, fps, memory_usage, model_name
            )

            cv2.imshow("YOLOv8 Object Detection", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Error during video processing: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()


def main():
    try:
        args = parse_arguments()
        model_file = get_model_filename(args.model)
        model = load_yolo_model(model_file, args.model)
        cap = initialize_webcam()
        process_video_stream(model, cap, args.model)

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
