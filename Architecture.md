# DeepGuard Architecture Documentation

## Overview

DeepGuard uses a three-tier architecture:

```text
React Frontend
FastAPI Backend
MySQL Database + File Storage
```

---

## Presentation Layer

Technology:

- React
- Vite
- Axios

Responsibilities:

- Login and registration UI
- Media upload form
- Scan history
- PDF download
- User role display

---

## Backend Layer

Technology:

- FastAPI
- Python 3.11
- SQLAlchemy
- JWT
- ReportLab

Responsibilities:

- Authentication
- JWT validation
- File upload handling
- AI inference routing
- Database insert/retrieval
- PDF report generation

---

## AI Detection Layer

Location:

```text
backend/app/services/detector.py
```

### Image Pipeline

```text
Image upload
↓
Pillow loads image
↓
Pretrained image deepfake model
↓
Real/Fake + confidence
```

### Video Pipeline

```text
Video upload
↓
OpenCV extracts representative frames
↓
Each frame passes through image model
↓
Scores are aggregated
↓
Real/Fake + confidence
```

### Audio Pipeline

```text
Audio upload
↓
Pretrained audio deepfake model
↓
Real/Fake + confidence
```

---

## Data Layer

Database:

```text
MySQL / XAMPP
```

Tables:

```text
users
scans
```

Files are not stored as Base64 or BLOBs. Files are stored on disk, and MySQL stores metadata and paths.

---

## File Storage

```text
backend/uploads/images/
backend/uploads/videos/
backend/uploads/audio/
backend/uploads/reports/
```

---

## Security

- Password hashing with bcrypt
- JWT token authentication
- Admin email whitelist
- Protected scan and report routes
- PDF download requires login token

---

## Future Enhancements

- Fine-tuned EfficientNet-B4 model trained on FaceForensics++ and DFDC
- Grad-CAM heatmap visualization
- PostgreSQL production database
- Docker deployment
- Cloud object storage
- Model evaluation dashboard
