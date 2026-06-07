# DeepGuard

DeepGuard is a web-based capstone project for analyzing possible deepfake media content involving government officials. It supports user login, role-based access, image/video/audio uploads, scan history, MySQL database storage, and PDF report generation.

> Current version uses a placeholder/mock detector. The web app workflow is working, but the real AI model such as EfficientNet-B4, Grad-CAM, video frame analysis, and audio deepfake model must be integrated later.

---

## Features

- React frontend
- FastAPI backend
- MySQL database using XAMPP
- JWT login authentication
- Admin email whitelist
- Upload image, video, and audio files
- Store files on disk
- Store metadata and scan results in MySQL
- Scan history table
- PDF report download
- Windows local development support

---

## Current Status

Working:

- Login
- Register
- Admin role detection
- Media upload
- Scan history
- Database insert
- PDF report generation
- PDF download with login token
- MySQL connection through XAMPP

Not yet real AI:

- EfficientNet-B4 deepfake detection
- Grad-CAM heatmap
- Real video frame deepfake detection
- Real audio deepfake recognition

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
│   │   ├── main.jsx
│   │   └── style.css
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   └── services/
│   │       └── detector.py
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

## System Architecture

```text
+----------------------+
|      React UI        |
|  Vite + Axios        |
+----------+-----------+
           |
           | REST API
           v
+----------------------+
|      FastAPI         |
| Auth / Upload / PDF  |
+----------+-----------+
           |
           +----------------------+
           |                      |
           v                      v
+----------------+       +------------------+
|     MySQL      |       |  File Storage    |
| Users          |       | Images           |
| Scans          |       | Videos           |
| Results        |       | Audio            |
| Reports Data   |       | PDF Reports      |
+----------------+       +------------------+
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
FastAPI validates request
   |
   v
File is saved to uploads folder
   |
   v
Mock detector generates result
   |
   v
Result and metadata saved to MySQL
   |
   v
PDF report is generated
   |
   v
Result appears in dashboard and scan history
```

---

# Installation Guide

## Required Software

Install the following:

- Python 3.11
- Node.js LTS
- XAMPP
- Visual Studio Code
- Git

Recommended Python version:

```text
Python 3.11.9
```

Do not use Python 3.13 for this project because some packages may have compatibility issues.

---

## Step 1: Start XAMPP

Open XAMPP Control Panel.

Start:

```text
Apache
MySQL
```

Open phpMyAdmin:

```text
http://localhost/phpmyadmin
```

---

## Step 2: Create Database

In phpMyAdmin, create a database:

```text
deepguard_db
```

Then import:

```text
database/deepguard_db.sql
```

---

## Step 3: Configure Backend Environment

Open:

```text
backend/.env
```

Example configuration:

```env
APP_NAME=DeepGuard
SECRET_KEY=change-this-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=1440
DATABASE_URL=mysql+pymysql://root:your_password@127.0.0.1:3306/deepguard_db
UPLOAD_DIR=uploads
ALLOWED_ADMIN_EMAILS=admin@deepguard.local,your_email@gmail.com
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

If your MySQL root has no password:

```env
DATABASE_URL=mysql+pymysql://root:@127.0.0.1:3306/deepguard_db
```

If your password has special characters, URL encode them.

Example:

```text
$ = %24
# = %23
@ = %40
```

---

## Step 4: Backend Setup

Open Command Prompt or PowerShell.

Go to backend folder:

```bash
cd backend
```

Create virtual environment using Python 3.11:

```bash
py -3.11 -m venv venv
```

Activate virtual environment:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

If bcrypt has issues, run:

```bash
pip uninstall bcrypt passlib -y
pip install "bcrypt==4.0.1" "passlib[bcrypt]==1.7.4"
```

Run backend:

```bash
python -m uvicorn app.main:app --reload
```

Open backend API docs:

```text
http://localhost:8000/docs
```

Expected result:

```text
FastAPI Swagger UI should appear.
```

---

## Step 5: Frontend Setup

Open another Command Prompt or PowerShell.

Go to frontend folder:

```bash
cd frontend
```

Install packages:

```bash
npm install
```

Run React development server:

```bash
npm run dev
```

Open frontend:

```text
http://localhost:5173
```

---

# Daily Startup Procedure

Every time you want to run the project:

## 1. Start XAMPP

Start:

```text
Apache
MySQL
```

## 2. Start Backend

```bash
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload
```

## 3. Start Frontend

Open another terminal:

```bash
cd frontend
npm run dev
```

Open:

```text
http://localhost:5173
```

---

# Login and Admin Setup

Admin users are controlled by:

```env
ALLOWED_ADMIN_EMAILS=
```

Example:

```env
ALLOWED_ADMIN_EMAILS=admin@deepguard.local,palaciodefaylona@gmail.com
```

Only emails listed there become admin.

All other registered users become normal users.

---

# File Storage Best Practice

DeepGuard does not store images, videos, or audio files directly inside the database.

Instead:

```text
uploads/images/
uploads/videos/
uploads/audio/
uploads/reports/
```

The database stores:

```text
filename
file path
media type
prediction
confidence
date created
report path
```

This is better than storing large files as Base64 or BLOBs.

---

# How to Test

## Test 1: Register

Register with an email.

Expected:

```text
User is created.
```

If the email is in `ALLOWED_ADMIN_EMAILS`, role should be:

```text
admin
```

Otherwise:

```text
user
```

---

## Test 2: Login

Login with your registered account.

Expected:

```text
Dashboard opens.
User email and role appear at the top.
```

---

## Test 3: Upload Image

Upload:

```text
.jpg
.jpeg
.png
```

Expected:

```text
Latest Result appears.
Scan History updates.
PDF button appears.
Record is inserted into MySQL.
```

---

## Test 4: Upload Video

Upload:

```text
.mp4
.avi
.mov
.mkv
```

Expected:

```text
Upload succeeds.
Result appears.
History updates.
```

---

## Test 5: Upload Audio

Upload:

```text
.mp3
.wav
.m4a
.flac
```

Expected:

```text
Upload succeeds.
Result appears.
History updates.
```

---

## Test 6: PDF Download

Click:

```text
PDF
```

or:

```text
Download PDF Report
```

Expected:

```text
PDF downloads successfully.
```

Important:

Do not manually open this in the browser:

```text
http://localhost:8000/scans/1/report
```

That direct URL will show:

```json
{"detail":"Missing login token"}
```

This happens because a direct browser URL does not include the JWT login token.

Use the PDF button inside the React app.

---

## Test 7: Database Check

Open:

```text
http://localhost/phpmyadmin
```

Go to:

```text
deepguard_db
```

Check:

```text
users
scans
```

Expected:

```text
users table contains registered users.
scans table contains uploaded file records.
```

---

## Test 8: Upload Folder Check

Go to:

```text
backend/uploads/
```

Expected uploaded files:

```text
images/
videos/
audio/
reports/
```

---

# Expected Output Example

After uploading an image:

```text
Latest Result

File: sample.jpg
Result: Real
Confidence: 71.97%
Explanation: Image facial-region analysis completed.
PDF Report: Available
```

Scan history should show:

```text
ID
File
Type
Result
Confidence
Date
Report
```

---

# Troubleshooting

## Uvicorn not found

Run:

```bash
python -m uvicorn app.main:app --reload
```

instead of:

```bash
uvicorn app.main:app --reload
```

## MySQL connection refused

Check:

- XAMPP MySQL is running
- Database exists
- `.env` uses correct password
- `DATABASE_URL` uses `127.0.0.1`

Example:

```env
DATABASE_URL=mysql+pymysql://root:password@127.0.0.1:3306/deepguard_db
```

---

## bcrypt error

Use Python 3.11 and run:

```bash
pip uninstall bcrypt passlib -y
pip install "bcrypt==4.0.1" "passlib[bcrypt]==1.7.4"
```

---

## Missing login token on upload

Clear browser storage, then login again.

Chrome:

```text
F12 → Application → Local Storage → Clear
```

Then login again.

---

## Missing login token on PDF

Use the PDF button inside the React app.

Do not open the backend report URL manually.

---

# Notes for Capstone Defense

The current version demonstrates:

- Web application implementation
- Authentication
- Role-based access
- File upload
- Database integration
- Scan history
- PDF report generation

The current AI detection is a placeholder.

For final defense, replace:

```text
backend/app/services/detector.py
```

with real AI model inference.

Recommended future AI implementation:

```text
Image: EfficientNet-B4 + Grad-CAM
Video: Frame extraction + EfficientNet-B4
Audio: Wav2Vec2 or RawNet2
```

---

# Disclaimer

This project is for academic and capstone development purposes. The current version uses mock AI detection and should not be used as a final real-world deepfake verification tool until trained and validated AI models are integrated.
