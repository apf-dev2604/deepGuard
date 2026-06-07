## System Architecture

```text
+----------------------+
|      React UI        |
|  (Vite + Axios)      |
+----------+-----------+
           |
           | HTTP / REST API
           |
           v
+----------------------+
|      FastAPI         |
| Authentication       |
| Upload Processing    |
| Report Generation    |
+----------+-----------+
           |
           |
           +---------------------+
           |                     |
           v                     v

+----------------+      +------------------+
|     MySQL      |      |  File Storage    |
| Users          |      | Images           |
| Scan History   |      | Videos           |
| Results        |      | Audio            |
+----------------+      | PDF Reports      |
                        +--------+---------+
                                 |
                                 v

                     +----------------------+
                     | AI Detection Engine  |
                     | EfficientNet-B4      |
                     | Wav2Vec2             |
                     | Grad-CAM             |
                     +----------------------+
```
