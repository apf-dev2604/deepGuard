from pathlib import Path
import hashlib
import random

IMAGE_EXT = {".jpg", ".jpeg", ".png"}
VIDEO_EXT = {".mp4", ".avi", ".mov", ".mkv"}
AUDIO_EXT = {".mp3", ".wav", ".m4a", ".flac"}

def get_modality(filename: str) -> str:
    ext = Path(filename).suffix.lower()
    if ext in IMAGE_EXT:
        return "image"
    if ext in VIDEO_EXT:
        return "video"
    if ext in AUDIO_EXT:
        return "audio"
    return "unknown"

def analyze_file(file_path: str, original_filename: str) -> dict:
    """
    MOCK DETECTOR for development and QA.
    Replace this function with real EfficientNet-B4/video/audio model inference later.
    It is deterministic for the same file, not truly random.
    """
    modality = get_modality(original_filename)
    data = Path(file_path).read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    seed = int(digest[:12], 16)
    rng = random.Random(seed)
    confidence = round(rng.uniform(61.0, 98.5), 2)
    prediction = "Fake" if seed % 2 == 0 else "Real"
    if modality == "image":
        explanation = "Image facial-region analysis completed. Grad-CAM placeholder is available for future model integration."
    elif modality == "video":
        explanation = "Video frame sampling completed. This starter build uses a mock video detector until the trained model is connected."
    elif modality == "audio":
        explanation = "Audio waveform feature extraction placeholder completed. This starter build is ready for audio deepfake model integration."
    else:
        explanation = "Unsupported file type."
    return {"prediction": prediction, "confidence": confidence, "modality": modality, "explanation": explanation}
