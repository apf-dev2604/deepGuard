"""
DeepGuard real AI detector service.

This module replaces the old mock detector. It uses free pretrained models for
local inference:
- Image: Hugging Face image-classification deepfake detector
- Video: OpenCV frame extraction + image detector aggregation
- Audio: Hugging Face audio-classification deepfake detector

The first scan can be slow because model files are downloaded and cached.
Use Python 3.11 for best Windows compatibility.
"""

import os
import tempfile
from pathlib import Path
from typing import Any, Dict, List

import cv2
import numpy as np
import torch
from PIL import Image
from transformers import pipeline


IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".flac"}

IMAGE_MODEL_ID = os.getenv("IMAGE_MODEL_ID", "nikokons/contrastive-deepfake-detector")
AUDIO_MODEL_ID = os.getenv("AUDIO_MODEL_ID", "Hemgg/Deepfake-audio-detection")
VIDEO_MAX_FRAMES = int(os.getenv("VIDEO_MAX_FRAMES", "8"))

_image_classifier = None
_audio_classifier = None


def get_device() -> int:
    """Return GPU device index when CUDA is available, otherwise CPU."""
    return 0 if torch.cuda.is_available() else -1


def get_image_classifier():
    global _image_classifier
    if _image_classifier is None:
        _image_classifier = pipeline(
            task="image-classification",
            model=IMAGE_MODEL_ID,
            device=get_device(),
        )
    return _image_classifier


def get_audio_classifier():
    global _audio_classifier
    if _audio_classifier is None:
        _audio_classifier = pipeline(
            task="audio-classification",
            model=AUDIO_MODEL_ID,
            device=get_device(),
        )
    return _audio_classifier


def normalize_label(label: str) -> str:
    text = str(label).lower()
    if any(word in text for word in ["fake", "deepfake", "ai", "spoof", "generated"]):
        return "Fake"
    if any(word in text for word in ["real", "bonafide", "bona fide", "genuine", "human"]):
        return "Real"
    return str(label).title()


def classify_image(image_path: str) -> Dict[str, Any]:
    classifier = get_image_classifier()
    image = Image.open(image_path).convert("RGB")
    results = classifier(image)

    if not results:
        raise ValueError("Image model returned no result.")

    top = results[0]
    prediction = normalize_label(top.get("label", "Unknown"))
    confidence = round(float(top.get("score", 0)) * 100, 2)

    return {
        "prediction": prediction,
        "confidence": confidence,
        "explanation": (
            "Image analyzed using a pretrained deepfake image classification model. "
            "This is real model inference, not a mock result."
        ),
        "model_used": IMAGE_MODEL_ID,
        "raw_results": results,
    }


def extract_video_frames(video_path: str, max_frames: int = VIDEO_MAX_FRAMES) -> List[str]:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Unable to open video file.")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames <= 0:
        cap.release()
        raise ValueError("Video has no readable frames.")

    frame_indexes = np.linspace(0, total_frames - 1, num=min(max_frames, total_frames))
    frame_indexes = [int(i) for i in frame_indexes]

    temp_dir = tempfile.mkdtemp(prefix="deepguard_frames_")
    saved_frames = []

    for index in frame_indexes:
        cap.set(cv2.CAP_PROP_POS_FRAMES, index)
        success, frame = cap.read()
        if not success:
            continue

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_path = os.path.join(temp_dir, f"frame_{index}.jpg")
        Image.fromarray(frame_rgb).save(frame_path)
        saved_frames.append(frame_path)

    cap.release()

    if not saved_frames:
        raise ValueError("No readable frames extracted from video.")

    return saved_frames


def classify_video(video_path: str) -> Dict[str, Any]:
    frames = extract_video_frames(video_path, max_frames=VIDEO_MAX_FRAMES)

    frame_results = []
    fake_scores = []
    real_scores = []

    for frame_path in frames:
        result = classify_image(frame_path)
        frame_results.append({
            "prediction": result["prediction"],
            "confidence": result["confidence"],
            "model_used": result["model_used"],
        })

        if result["prediction"] == "Fake":
            fake_scores.append(result["confidence"])
            real_scores.append(100 - result["confidence"])
        elif result["prediction"] == "Real":
            real_scores.append(result["confidence"])
            fake_scores.append(100 - result["confidence"])
        else:
            fake_scores.append(50)
            real_scores.append(50)

    avg_fake = sum(fake_scores) / len(fake_scores)
    avg_real = sum(real_scores) / len(real_scores)

    if avg_fake >= avg_real:
        prediction = "Fake"
        confidence = round(avg_fake, 2)
    else:
        prediction = "Real"
        confidence = round(avg_real, 2)

    return {
        "prediction": prediction,
        "confidence": confidence,
        "explanation": (
            f"Video analyzed by extracting {len(frames)} representative frames "
            "with OpenCV and classifying each frame using the pretrained image "
            "deepfake detector. Frame scores were aggregated into one result."
        ),
        "model_used": IMAGE_MODEL_ID,
        "frames_analyzed": len(frames),
        "frame_results": frame_results,
    }


def classify_audio(audio_path: str) -> Dict[str, Any]:
    classifier = get_audio_classifier()
    results = classifier(audio_path)

    if not results:
        raise ValueError("Audio model returned no result.")

    top = results[0]
    prediction = normalize_label(top.get("label", "Unknown"))
    confidence = round(float(top.get("score", 0)) * 100, 2)

    return {
        "prediction": prediction,
        "confidence": confidence,
        "explanation": (
            "Audio analyzed using a pretrained Wav2Vec2-based deepfake audio "
            "classification model. This is real model inference, not a mock result."
        ),
        "model_used": AUDIO_MODEL_ID,
        "raw_results": results,
    }


def detect_media(file_path: str) -> Dict[str, Any]:
    extension = Path(file_path).suffix.lower()

    if extension in IMAGE_EXTENSIONS:
        result = classify_image(file_path)
        result["modality"] = "image"
        return result

    if extension in VIDEO_EXTENSIONS:
        result = classify_video(file_path)
        result["modality"] = "video"
        return result

    if extension in AUDIO_EXTENSIONS:
        result = classify_audio(file_path)
        result["modality"] = "audio"
        return result

    raise ValueError(f"Unsupported file type: {extension}")


# Compatibility aliases for older backend code names.
def analyze_media(file_path: str) -> Dict[str, Any]:
    return detect_media(file_path)


def analyze_file(file_path: str) -> Dict[str, Any]:
    return detect_media(file_path)
