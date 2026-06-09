# DeepGuard

DeepGuard is a web-based capstone project for detecting possible deepfake media involving government officials. This package includes a React frontend, FastAPI backend, XAMPP/MySQL database support, file upload, scan history, PDF reports, and real pretrained AI inference for image, video, and audio analysis.

> This version replaces the mock detector with pretrained AI models. The first scan can take time because model files are downloaded from Hugging Face and cached locally.

---

## Features

- React + Vite frontend
- FastAPI backend
- MySQL database using XAMPP
- JWT login authentication
- Admin email whitelist
- Image, video, and audio uploads
- Real pretrained AI inference
- Video frame extraction using OpenCV
- Audio deepfake classification using pretrained audio model
- File storage on disk
- Metadata and scan results in MySQL
- Scan history table
- PDF report download with login token
- Windows local deployment

---

## Current AI Implementation

Image uploads are analyzed using a pretrained Hugging Face image deepfake classification model.

Video uploads are processed by extracting representative frames with OpenCV, running each frame through the image detector, and aggregating the frame-level scores.

Audio uploads are analyzed using a pretrained Hugging Face audio deepfake classification model.

This is real model inference, not random/mock output. However, results are still probabilistic and should be validated through formal testing before real-world use.

---

## Directory Tree

```text
deepguard/
├── README.md
├── INSTALLATION.md
├── TESTING.md
├── ARCHITECTURE.md
├── .gitignore
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   └── src/
│       ├── main.jsx
│       └── style.css
│
├── backend/
│   ├── .env.example
│   ├── requirements.txt
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── services/
│   │       ├── __init__.py
│   │       └── detector.py
│   │
│   └── uploads/
│       ├── images/
│       ├── videos/
│       ├── audio/
│       └── reports/
│
├── database/
│   └── deepguard_db.sql
│
└── docs/
    ├── screenshots/
    ├── diagrams/
    └── references/
```

---

## System Workflow

```text
User Login
   |
   v
Upload Image / Video / Audio
   |
   v
FastAPI validates JWT token
   |
   v
File is saved to uploads folder
   |
   v
Real pretrained AI detector runs
   |
   +--> Image: image model inference
   +--> Video: OpenCV frame extraction + image model inference
   +--> Audio: audio model inference
   |
   v
Result and metadata saved to MySQL
   |
   v
PDF report generated
   |
   v
Result appears in dashboard and scan history
```

---

## Quick Start

1. Start XAMPP Apache and MySQL.
2. Import `database/deepguard_db.sql` in phpMyAdmin.
3. Copy `backend/.env.example` to `backend/.env` and update your MySQL password.
4. Start backend:

```bash
cd backend
py -3.11 -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

5. Start frontend:

```bash
cd frontend
npm install
npm run dev
```

6. Open:

```text
http://localhost:5173
```

Backend docs:

```text
http://localhost:8000/docs
```

---

## Important Notes

Use Python 3.11. Avoid Python 3.13 for this project because some AI and authentication packages may have compatibility issues.

The first AI scan may take several minutes depending on your internet speed and laptop performance because pretrained model files must be downloaded.

For videos, short clips are recommended. Long videos are slower because frames need to be extracted and analyzed.

---

## Capstone Scope Note

The original PPTX focused on image and video deepfake detection using EfficientNet-B4, OpenCV, and Grad-CAM. This package extends the system with audio/voice deepfake detection using a pretrained audio classification model.
