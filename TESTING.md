# DeepGuard Testing Guide

## Authentication Tests

### Register Admin

Use an email listed in `ALLOWED_ADMIN_EMAILS`.

Expected:

```text
Role = admin
```

### Register Normal User

Use an email not listed in `ALLOWED_ADMIN_EMAILS`.

Expected:

```text
Role = user
```

### Login Success

Expected:

```text
Dashboard opens
JWT token saved
User email and role visible
```

### Login Failure

Use wrong password.

Expected:

```text
Invalid email or password
```

---

## Upload Tests

### Image Upload

Use:

```text
.jpg
.jpeg
.png
```

Expected:

```text
Real AI image detector runs
Latest result appears
Scan history updates
PDF report available
Database row inserted
```

### Video Upload

Use short clips:

```text
.mp4
.avi
.mov
.mkv
```

Expected:

```text
OpenCV extracts frames
Each frame is analyzed
Aggregated result appears
PDF report available
```

### Audio Upload

Use:

```text
.mp3
.wav
.m4a
.flac
```

Expected:

```text
Audio model runs
Real/Fake result appears
PDF report available
```

---

## PDF Test

Click the PDF button inside the React app.

Expected:

```text
PDF downloads successfully
```

Do not manually open `/scans/1/report` in the browser address bar because direct browser navigation does not include the JWT token.

---

## Database Test

Open:

```text
http://localhost/phpmyadmin
```

Check:

```text
deepguard_db.users
deepguard_db.scans
```

Expected:

```text
Registered users exist
Scan records exist
Model used is saved
Prediction and confidence are saved
```

---

## Expected Output Example

```text
File: sample.jpg
Type: image
Result: Fake
Confidence: 92.31%
Model: nikokons/contrastive-deepfake-detector
PDF: Available
```

---

## Notes

The first AI scan can be slow because model files download first. Later scans are faster because models are cached locally.
