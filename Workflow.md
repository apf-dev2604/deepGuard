## System Workflow

```text
User Login
     |
     v
Upload Media
(Image/Video/Audio)
     |
     v
Backend Validation
     |
     v
Save File to Upload Folder
     |
     v
AI Analysis
     |
     +---------------------+
     |                     |
     v                     v

Real                Fake
     |                     |
     +----------+----------+
                |
                v

Generate Result
(Confidence Score)

                |
                v

Generate PDF Report

                |
                v

Save Scan History

                |
                v

Display Result to User
```
