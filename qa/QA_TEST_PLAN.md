# DeepGuard QA Test Plan

## Smoke Test
1. Start XAMPP Apache and MySQL.
2. Import database/deepguard_db.sql in phpMyAdmin.
3. Run start-backend.bat.
4. Open http://localhost:8000/docs.
5. Run start-frontend.bat.
6. Open http://localhost:5173.

## Functional Tests
- Register new user: should become viewer unless email is in ALLOWED_ADMIN_EMAILS.
- Login with valid credentials: should open dashboard.
- Login with wrong password: should show error.
- Upload JPG/PNG: should create image scan.
- Upload MP4/MOV/AVI/MKV: should create video scan.
- Upload MP3/WAV/M4A/FLAC: should create audio scan.
- Upload unsupported file: should reject.
- Download PDF report: should open/download PDF.
- Viewer account: should only see own scans.
- Admin account: should see all scans.

## Database Checks
In phpMyAdmin, check these tables after using the app:
- users
- scans

Files should be stored in backend/uploads, not directly as Base64 in the database.
