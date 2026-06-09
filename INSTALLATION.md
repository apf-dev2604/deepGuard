# DeepGuard Installation Guide

## Required Software

Install:

- Python 3.11
- Node.js LTS
- XAMPP
- Git
- Visual Studio Code

Recommended Python version:

```text
Python 3.11.9
```

Avoid Python 3.13 for this project.

---

## 1. Start XAMPP

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

## 2. Create Database

Import this file:

```text
database/deepguard_db.sql
```

This creates:

```text
deepguard_db
users table
scans table
```

---

## 3. Configure Backend Environment

Copy:

```text
backend/.env.example
```

to:

```text
backend/.env
```

Example with no MySQL root password:

```env
DATABASE_URL=mysql+pymysql://root:@127.0.0.1:3306/deepguard_db
```

Example with MySQL password:

```env
DATABASE_URL=mysql+pymysql://root:your_password@127.0.0.1:3306/deepguard_db
```

If your password contains special characters, URL encode them.

```text
$ = %24
# = %23
@ = %40
```

---

## 4. Backend Setup

Open Command Prompt or PowerShell.

```bash
cd backend
py -3.11 -m venv venv
venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

If bcrypt causes issues:

```bash
pip uninstall bcrypt passlib -y
pip install "bcrypt==4.0.1" "passlib[bcrypt]==1.7.4"
```

Run backend:

```bash
python -m uvicorn app.main:app --reload
```

Open:

```text
http://localhost:8000/docs
```

---

## 5. Frontend Setup

Open a second terminal.

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

---

## Daily Startup

Start XAMPP Apache and MySQL.

Backend:

```bash
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm run dev
```

---

## Windows Server Mode

For access from another device on the same network:

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Then update frontend API URL if needed.
