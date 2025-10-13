# YOLOv8 Object Detection - Edge AI Demo

Real-time object detection demonstrating Edge AI concepts: model size trade-offs, performance constraints, and local inference.

This demo uses YOLOv8 models from [Ultralytics](https://ultralytics.com/), a leading computer vision AI company that provides state-of-the-art YOLO models for object detection.

## Hardware Requirements:
- Laptop or Computer (MacOS Apple silicon, Linux, Windows)
- Built-in camera or webcam

## Key Concept: Edge AI Trade-offs

Edge AI runs AI models locally instead of cloud servers. This demo runs on your laptop for development and testing, simulating what will happen when deployed to edge devices like Raspberry Pi. 

**Development Workflow**: The same code can run on a Raspberry Pi using containers or direct deployment - we're testing on a development machine first to understand performance characteristics before actual edge deployment.

*Note: Full Raspberry Pi deployment examples will be covered in future updates to this repository.*

**Two models to compare:**

| Model | Size | Speed | Accuracy | Resource Usage |
|-------|------|-------|----------|----------------|
| **medium** | ~52MB | Moderate | Higher | More CPU/RAM |
| **nano** | ~6MB | Fastest | Good | Less CPU/RAM |

*Other variants (small, large, xlarge) exist but we focus on these two to demonstrate the core trade-off.*

**Performance metrics overlay:**
- **Inference time**: Processing speed per frame
- **FPS**: Real-time capability  
- **RAM usage**: Memory consumption

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. **Test medium model first** (higher accuracy, more resources):
   ```bash
   python yolo_object_detection.py --model medium
   ```
   
   *Note: On first run, the model will be automatically downloaded (~52MB for medium). This requires an internet connection and may take a few moments.*
   
   **Observe the performance metrics** - note your inference time, FPS, and RAM usage. These represent the performance characteristics of a more accurate but resource-intensive model.

3. **Switch to nano model** (faster processing, fewer resources):
   ```bash
   python yolo_object_detection.py --model nano
   ```
   
   **Compare the metrics** - you should see faster inference times, higher FPS, and lower RAM usage compared to the medium model. The exact numbers will vary based on your machine, but the performance improvement trend will be consistent.

4. **Key observations to make**:
   - How much faster is inference time with nano vs. medium?
   - What's the FPS difference between the two models?
   - How much less RAM does the nano model use?
   - Is there a noticeable difference in detection accuracy?

Press 'q' to quit each test.

## Edge AI Learning Objectives

### 1. Experience the Core Trade-off
By running both models, you'll directly observe:
- **Medium model**: Higher accuracy, more resource usage
- **Nano model**: Faster processing, lower resource usage
- **Performance impact**: How model size affects inference speed, FPS, and memory

### 2. Understand Deployment Constraints
- **Development vs. Edge**: Laptop testing proves the code logic and integration work - if it fails on edge devices, it's almost always due to resource constraints
- **Code portability**: The same Python code can run on Pi using containers or direct deployment
- **Real-time requirements**: Some applications need consistent frame rates
For edge deployment, consider:
- **Target hardware**: Raspberry Pi vs. other embedded devices
- **Power constraints**: Battery life and power consumption on edge devices
- **Accuracy requirements**: Sometimes "good enough" is better than "perfect"
- **Real-time needs**: Can you afford 100ms latency or do you need <10ms?

### 3. Local Processing Benefits
This demo runs entirely offline, demonstrating:
- **Privacy**: No data sent to external servers
- **Latency**: No network delays
- **Reliability**: Works without internet connection
- **Cost**: No cloud API charges

## Real-World Edge AI Applications

This object detection demo simulates scenarios like:

- **Smart security cameras**: Detecting people/vehicles without cloud connectivity
- **Industrial inspection**: Quality control on manufacturing lines  
- **Retail analytics**: Customer behavior analysis at the edge
- **Agricultural monitoring**: Crop and livestock monitoring with drones

## Performance Optimization Tips

### For Edge Deployment:
1. **Start with nano model** - upgrade only if accuracy isn't sufficient
2. **Monitor memory usage** - ensure it fits your target device
3. **Test thermal performance** - sustained processing may cause throttling
4. **Consider quantization** - further reduce model size if needed
5. **Optimize input resolution** - lower resolution = faster processing

## Controls

- **Press 'q'**: Quit the application
- **Webcam required**: Make sure your camera is connected and accessible

## Troubleshooting

### Common Issues:
- **Webcam not found**: Check camera permissions and connections
- **Low FPS**: Try a smaller model (nano/small) or reduce resolution
- **High memory usage**: Switch to a smaller model variant
- **Model download fails**: Check internet connection for initial download

### Performance Tips:
- Close other applications to free up system resources
- Ensure good lighting for better detection accuracy
- Position camera for optimal viewing angle

This demo provides hands-on experience with the core challenges and trade-offs in Edge AI deployment. You're testing the same code that can run on edge devices like Raspberry Pi, using your laptop as a development environment to understand performance characteristics before actual deployment.

**Future Examples**: Complete Raspberry Pi deployment tutorials (including containerization and optimization) will be added to this repository in future updates.