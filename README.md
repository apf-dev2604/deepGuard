# DeepGuard

## AI-Based Deepfake Detection System for Government Officials' Media Content

DeepGuard is a web-based deepfake detection platform designed to help citizens, journalists, researchers, and government agencies analyze media content that may contain manipulated images, videos, or audio.

The project was developed as a BS Information Technology Capstone Project and provides a secure platform for media uploads, scan history management, PDF report generation, and future integration with AI-powered deepfake detection models.

---

## Project Overview

DeepGuard addresses the growing problem of deepfake disinformation targeting government officials and public figures.

The system allows users to:

* Upload images, videos, and audio files
* Perform media analysis
* View scan history
* Generate downloadable PDF reports
* Manage users through role-based access control

The current version includes a complete web application workflow and is prepared for integration with machine learning models such as EfficientNet-B4 and Wav2Vec2.

---

## Directory Tree

```text
deepguard/
├── README.md
├── INSTALLATION.md
├── TESTING.md
├── ARCHITECTURE.md
├── LICENSE
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── app/
│   │   ├── services/
│   │   ├── routes/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── main.py
│   │
│   ├── uploads/
│   │   ├── images/
│   │   ├── videos/
│   │   ├── audio/
│   │   └── reports/
│   │
│   ├── requirements.txt
│   └── .env
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

## Features

### Authentication

* User Registration
* User Login
* JWT Authentication
* Role-Based Access Control
* Admin Email Whitelisting

### Media Analysis

Supported File Types:

#### Images

* JPG
* JPEG
* PNG

#### Videos

* MP4
* AVI
* MOV
* MKV

#### Audio

* MP3
* WAV
* M4A
* FLAC

### Reports

* Scan History
* PDF Report Generation
* Timestamped Analysis Results

### Administration

* User Management
* Admin Whitelist Configuration
* Protected API Endpoints

---

## Technology Stack

### Frontend

* React
* Vite
* Axios
* Lucide React

### Backend

* FastAPI
* Python
* SQLAlchemy
* JWT Authentication

### Database

* MySQL (XAMPP)

### Planned AI Models

#### Image Deepfake Detection

* EfficientNet-B4
* OpenCV
* Grad-CAM

#### Video Deepfake Detection

* Frame Extraction
* Face Detection
* EfficientNet-B4 Inference

#### Audio Deepfake Detection

* Wav2Vec2
* RawNet2

---

## Project Structure

deepguard/

frontend/
src/
public/

backend/
app/
services/
uploads/

database/

README.md

---

## Installation

### Requirements

* Python 3.11
* Node.js LTS
* XAMPP
* MySQL

---

### Clone Repository

git clone https://github.com/your-repository/deepguard.git

cd deepguard

---

## Database Setup

Start:

* Apache
* MySQL

from XAMPP Control Panel.

Open:

http://localhost/phpmyadmin

Create:

deepguard_db

Import:

database/deepguard_db.sql

---

## Backend Installation

Navigate to backend folder:

cd backend

Create virtual environment:

py -3.11 -m venv venv

Activate:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run backend:

python -m uvicorn app.main:app --reload

Backend API:

http://localhost:8000

Swagger Documentation:

http://localhost:8000/docs

---

## Frontend Installation

Navigate to frontend:

cd frontend

Install dependencies:

npm install

Run development server:

npm run dev

Frontend:

http://localhost:5173

---

## Configuration

Update backend .env:

APP_NAME=DeepGuard

SECRET_KEY=your-secret-key

DATABASE_URL=mysql+pymysql://root:password@127.0.0.1:3306/deepguard_db

UPLOAD_DIR=uploads

ALLOWED_ADMIN_EMAILS=[admin@example.com](mailto:admin@example.com)

---

## Usage

### Register

Create a new account.

Only emails listed in:

ALLOWED_ADMIN_EMAILS

will receive Admin privileges.

All other users are assigned the User role.

---

### Login

Login using registered credentials.

Successful login generates a JWT access token.

---

### Upload Media

Upload:

* Images
* Videos
* Audio Files

Click:

Upload and Analyze

The system stores:

* Uploaded File
* Metadata
* Scan Results
* PDF Report

---

### View Scan History

The Scan History section displays:

* File Name
* Media Type
* Result
* Confidence Score
* Date Analyzed
* PDF Report Link

---

## Current Implementation

The current version contains:

* Authentication
* User Management
* Upload Management
* Database Integration
* Scan History
* PDF Reports

The detector currently uses a placeholder implementation for demonstration purposes.

---

## Planned AI Integration

Future versions will replace the placeholder detector with:

### Images

EfficientNet-B4

Outputs:

* Real/Fake Classification
* Confidence Score
* Grad-CAM Visualization

### Videos

Process:

Video → Frame Extraction → Face Detection → Deepfake Analysis

Outputs:

* Real/Fake Classification
* Suspicious Frame Identification

### Audio

Outputs:

* Real/Fake Classification
* Confidence Score
* Waveform Analysis

---

## Testing

### Functional Testing

#### Authentication

* Login with valid credentials
* Login with invalid credentials
* Register new user
* Logout

#### Upload Testing

* JPG Upload
* PNG Upload
* MP4 Upload
* MP3 Upload
* Empty Upload Validation

#### Reports

* PDF Generation
* PDF Download

#### Database

* User Creation
* Scan Record Creation
* History Retrieval

---

## Expected Output

After a successful upload:

* File is stored in uploads folder
* Scan result is displayed
* Scan history is updated
* PDF report is generated
* Database record is created

Example:

Result: Real

Confidence: 71.97%

Media Type: Image

Report: PDF Available

---

## Security

* JWT Authentication
* Password Hashing using bcrypt
* Role-Based Authorization
* Admin Email Whitelisting
* Protected API Endpoints

---

## Authors

BS Information Technology

Capstone Project

Polytechnic University of the Philippines

Academic Year 2025–2026

---

## Disclaimer

This project is intended for academic and research purposes.

The current implementation contains placeholder detection logic and serves as a foundation for future AI-powered deepfake detection integration.

