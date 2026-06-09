import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import jwt
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from passlib.context import CryptContext
from pydantic import BaseModel
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.services.detector import detect_media

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "DeepGuard")
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:@127.0.0.1:3306/deepguard_db")
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads"))
ALLOWED_ADMIN_EMAILS = [e.strip().lower() for e in os.getenv("ALLOWED_ADMIN_EMAILS", "admin@deepguard.local").split(",") if e.strip()]
CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",") if o.strip()]

for folder in ["images", "videos", "audio", "reports"]:
    (UPLOAD_DIR / folder).mkdir(parents=True, exist_ok=True)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    role = Column(String(50), default="user", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Scan(Base):
    __tablename__ = "scans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    original_filename = Column(String(255), nullable=False)
    stored_filename = Column(String(255), nullable=False)
    file_path = Column(Text, nullable=False)
    modality = Column(String(50), nullable=False)
    prediction = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    explanation = Column(Text, nullable=True)
    model_used = Column(String(255), nullable=True)
    report_path = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


class RegisterRequest(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None


class LoginRequest(BaseModel):
    email: str
    password: str


app = FastAPI(title=APP_NAME)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing login token")

    token = authorization.replace("Bearer ", "", 1)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def user_to_dict(user: User) -> dict:
    return {"id": user.id, "email": user.email, "full_name": user.full_name, "role": user.role}


def safe_filename(filename: str) -> str:
    name = Path(filename).name.replace(" ", "_")
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-"
    return "".join(c for c in name if c in allowed) or "uploaded_file"


def folder_for_extension(extension: str) -> str:
    if extension in {".jpg", ".jpeg", ".png"}:
        return "images"
    if extension in {".mp4", ".avi", ".mov", ".mkv"}:
        return "videos"
    if extension in {".mp3", ".wav", ".m4a", ".flac"}:
        return "audio"
    raise HTTPException(status_code=400, detail=f"Unsupported file type: {extension}")


def generate_report(scan: Scan) -> str:
    report_name = f"deepguard_report_{scan.id}.pdf"
    report_path = UPLOAD_DIR / "reports" / report_name

    c = canvas.Canvas(str(report_path), pagesize=letter)
    width, height = letter

    y = height - 60
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, "DeepGuard Analysis Report")

    y -= 40
    c.setFont("Helvetica", 11)
    lines = [
        f"Scan ID: {scan.id}",
        f"Original File: {scan.original_filename}",
        f"Media Type: {scan.modality}",
        f"Prediction: {scan.prediction}",
        f"Confidence: {scan.confidence}%",
        f"Model Used: {scan.model_used or 'N/A'}",
        f"Created At: {scan.created_at}",
        "",
        "Explanation:",
        scan.explanation or "No explanation available.",
        "",
        "Note: Deepfake detection outputs are probabilistic and should be used with",
        "human review, fact-checking, and supporting evidence.",
    ]

    for line in lines:
        if y < 80:
            c.showPage()
            y = height - 60
            c.setFont("Helvetica", 11)
        c.drawString(50, y, str(line)[:100])
        y -= 18

    c.save()
    return str(report_path)


def scan_to_dict(scan: Scan) -> dict:
    return {
        "id": scan.id,
        "original_filename": scan.original_filename,
        "stored_filename": scan.stored_filename,
        "modality": scan.modality,
        "prediction": scan.prediction,
        "confidence": scan.confidence,
        "explanation": scan.explanation,
        "model_used": scan.model_used,
        "created_at": scan.created_at.isoformat(),
        "report_url": f"/scans/{scan.id}/report",
    }


@app.get("/")
def root():
    return {"app": APP_NAME, "status": "running", "detector": "pretrained real AI inference"}


@app.post("/auth/register")
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    email = payload.email.strip().lower()
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    role = "admin" if email in ALLOWED_ADMIN_EMAILS else "user"
    user = User(email=email, full_name=payload.full_name, password_hash=hash_password(payload.password), role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Registered successfully", "user": user_to_dict(user)}


@app.post("/auth/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    email = payload.email.strip().lower()
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": str(user.id), "email": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer", "user": user_to_dict(user)}


@app.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return user_to_dict(current_user)


@app.post("/scans")
def create_scan(file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    extension = Path(file.filename or "").suffix.lower()
    folder = folder_for_extension(extension)

    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    stored_filename = f"{timestamp}_{safe_filename(file.filename or 'upload') }"
    save_path = UPLOAD_DIR / folder / stored_filename

    with save_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        result = detect_media(str(save_path))
    except Exception as exc:
        # Keep file for debugging, but fail the request with a clear message.
        raise HTTPException(status_code=500, detail=f"AI detection failed: {exc}")

    scan = Scan(
        user_id=current_user.id,
        original_filename=file.filename or stored_filename,
        stored_filename=stored_filename,
        file_path=str(save_path),
        modality=result.get("modality", folder),
        prediction=result.get("prediction", "Unknown"),
        confidence=float(result.get("confidence", 0)),
        explanation=result.get("explanation", ""),
        model_used=result.get("model_used", ""),
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)

    report_path = generate_report(scan)
    scan.report_path = report_path
    db.commit()
    db.refresh(scan)

    return scan_to_dict(scan)


@app.get("/scans")
def list_scans(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    query = db.query(Scan)
    if current_user.role != "admin":
        query = query.filter(Scan.user_id == current_user.id)
    scans = query.order_by(Scan.created_at.desc()).all()
    return [scan_to_dict(scan) for scan in scans]


@app.get("/scans/{scan_id}/report")
def get_report(scan_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    if current_user.role != "admin" and scan.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    if not scan.report_path or not Path(scan.report_path).exists():
        raise HTTPException(status_code=404, detail="Report file not found")
    return FileResponse(scan.report_path, media_type="application/pdf", filename=f"deepguard-report-{scan.id}.pdf")
