import os
import shutil
from pathlib import Path
from uuid import uuid4
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional
from app.db.database import get_db
from app.db.init_db import init_db
from app.db.models import User, Scan
from app.services.auth import hash_password, verify_password, create_access_token, decode_token
from app.services.detector import analyze_file, get_modality
from app.services.reports import create_scan_report

load_dotenv()
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
ALLOWED_ADMIN_EMAILS = [e.strip().lower() for e in os.getenv("ALLOWED_ADMIN_EMAILS", "admin@deepguard.local").split(",") if e.strip()]
CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")]

app = FastAPI(title="DeepGuard API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@app.on_event("startup")
def startup():
    init_db()
    Path(UPLOAD_DIR).mkdir(exist_ok=True)
    for sub in ["images", "videos", "audio", "reports"]:
        Path(UPLOAD_DIR, sub).mkdir(parents=True, exist_ok=True)


def current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing login token")
    token = authorization.split(" ", 1)[1]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired login token")
    user = db.query(User).filter(User.email == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@app.get("/")
def root():
    return {"message": "DeepGuard API is running", "docs": "/docs"}

@app.post("/auth/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    email = data.email.lower()
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    role = "admin" if email in ALLOWED_ADMIN_EMAILS else "viewer"
    user = User(email=email, full_name=data.full_name, password_hash=hash_password(data.password), role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": user.id, "email": user.email, "role": user.role, "message": "Registered successfully"}

@app.post("/auth/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email.lower()).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token(user.email, user.role)
    return {"access_token": token, "token_type": "bearer", "user": {"email": user.email, "role": user.role, "full_name": user.full_name}}

@app.get("/me")
def me(user: User = Depends(current_user)):
    return {"email": user.email, "role": user.role, "full_name": user.full_name}

@app.post("/scans")
def upload_scan(file: UploadFile = File(...), user: User = Depends(current_user), db: Session = Depends(get_db)):
    modality = get_modality(file.filename or "")
    if modality == "unknown":
        raise HTTPException(status_code=400, detail="Unsupported file type. Use JPG, PNG, MP4, AVI, MOV, MP3, WAV, M4A, or FLAC.")
    subdir = {"image": "images", "video": "videos", "audio": "audio"}[modality]
    ext = Path(file.filename).suffix.lower()
    stored_filename = f"{uuid4().hex}{ext}"
    destination = Path(UPLOAD_DIR, subdir, stored_filename)
    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    result = analyze_file(str(destination), file.filename)
    scan = Scan(user_id=user.id, original_filename=file.filename, stored_filename=stored_filename, file_path=str(destination).replace("\\", "/"), file_type=file.content_type or "application/octet-stream", modality=result["modality"], file_size=destination.stat().st_size, prediction=result["prediction"], confidence=result["confidence"], explanation=result["explanation"])
    db.add(scan)
    db.commit()
    db.refresh(scan)
    scan.report_path = create_scan_report(scan)
    db.commit()
    return scan_to_dict(scan)

@app.get("/scans")
def list_scans(user: User = Depends(current_user), db: Session = Depends(get_db)):
    q = db.query(Scan)
    if user.role != "admin":
        q = q.filter(Scan.user_id == user.id)
    scans = q.order_by(desc(Scan.created_at)).limit(100).all()
    return [scan_to_dict(s) for s in scans]

@app.get("/scans/{scan_id}/report")
def download_report(scan_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    if user.role != "admin" and scan.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    if not scan.report_path or not Path(scan.report_path).exists():
        scan.report_path = create_scan_report(scan)
        db.commit()
    return FileResponse(scan.report_path, media_type="application/pdf", filename=f"deepguard_scan_{scan.id}.pdf")

def scan_to_dict(scan: Scan):
    return {"id": scan.id, "original_filename": scan.original_filename, "file_type": scan.file_type, "modality": scan.modality, "file_size": scan.file_size, "prediction": scan.prediction, "confidence": scan.confidence, "explanation": scan.explanation, "created_at": scan.created_at.isoformat() if scan.created_at else None, "report_url": f"/scans/{scan.id}/report"}
