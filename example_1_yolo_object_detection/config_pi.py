"""
Configuration settings for the Raspberry Pi Camera Stream application.
"""
import os
import secrets
from typing import Tuple

class Config:
    """Simple configuration for development/testing."""
    
    # Camera Configuration
    CAMERA_RESOLUTION: Tuple[int, int] = (800, 600)
    CAMERA_FORMAT = "BGR888"
    CAMERA_FPS_LIMIT = 30
    
    # YOLO Configuration
    YOLO_MODEL_PATH = 'yolo11n.pt'
    YOLO_INPUT_SIZE = 800
    YOLO_ENABLED_DEFAULT = True
    
    # Streaming Configuration
    JPEG_QUALITY = 80
    FRAME_BUFFER_SIZE = 5
    
    # Server Configuration
    HOST = '0.0.0.0'
    PORT = 8080
    DEBUG = True
    
    # CORS Configuration (allow all for development)
    CORS_ORIGINS = '*'

# Use single config for simplicity
config = Config