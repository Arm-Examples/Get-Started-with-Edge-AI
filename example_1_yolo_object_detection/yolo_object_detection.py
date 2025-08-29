import cv2
import time
import psutil
import argparse
from ultralytics import YOLO

# Command line argument parsing
parser = argparse.ArgumentParser(description="YOLOv8 object detection with webcam")
parser.add_argument("--model", type=str, default="nano", 
                    help="YOLOv8 model size (nano, small, medium, large)")
args = parser.parse_args()

# Model mapping
model_map = {
    "nano": "yolov8n.pt",
    "small": "yolov8s.pt", 
    "medium": "yolov8m.pt",
    "large": "yolov8l.pt"
}

# Get model filename
if args.model in model_map:
    model_file = model_map[args.model]
else:
    # Fallback: assume it's a direct filename
    model_file = args.model

# Load YOLOv8 model
print(f"Loading {args.model} model: {model_file}")
model = YOLO(model_file)


# Access COCO class names
COCO_CLASSES = model.names

# Open default webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Could not open webcam.")
    exit()

print("✅ Webcam opened. Press 'q' to quit.")

# Performance tracking
frame_count = 0
start_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to grab frame.")
        break

    t0 = time.time()
    results = model(frame, verbose=False)
    t1 = time.time()

    # Inference time and FPS
    inference_time = t1 - t0
    fps = 1.0 / inference_time if inference_time > 0 else 0

    # RAM usage
    mem_usage = psutil.Process().memory_info().rss / (1024 * 1024)  # in MB

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = COCO_CLASSES[cls_id]
            conf = float(box.conf[0])

            # Draw bounding box and label
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Overlay performance stats
    stats_text = f"Inference: {inference_time * 1000:.1f}ms | FPS: {fps:.1f} | RAM: {mem_usage:.1f} MB"
    cv2.putText(frame, stats_text, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

    cv2.imshow("YOLOv8 Object Detection (Mac)", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()