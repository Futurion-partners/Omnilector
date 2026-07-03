# 📚 Complete Technical Documentation - Omnilector API

## 📋 Table of Contents

1. [Introduction](#-introduction)
2. [Features](#-features)
3. [System Architecture](#-system-architecture)
4. [System Requirements](#-system-requirements)
5. [Installation and Configuration](#-installation-and-configuration)
6. [Usage Guide](#-usage-guide)
7. [API Reference](#-api-reference)
8. [Web Client (Frontend)](#-web-client-frontend)
9. [Optimization and Performance](#-optimization-and-performance)
10. [Troubleshooting](#-troubleshooting)
11. [Development and Contribution](#-development-and-contribution)
12. [Production Deployment](#-production-deployment)

---

## 🎯 Introduction

**Omnilector** is a modern and efficient API for real-time barcode and QR code detection and decoding. Developed using **FastAPI** and **Python 3.13**, it offers two operating modes:

- **Image Mode**: Static image processing via a REST API.
- **Real-Time Mode**: Continuous detection via WebSockets with video stream frame-by-frame transmission.

### Use Cases

- Scanning 1D barcodes (EAN, UPC, Code128, etc.).
- Reading QR codes.
- Detecting Aztec and DataMatrix codes.
- Real-time inventory tracking applications.
- Access control systems utilizing QR codes.
- Point of sale (POS) systems.
- Product validation apps.

---

## ✨ Features

### Technical Highlights

- ✅ **Multi-engine detection**: Combines PyZbar, ZXing-C++, and OpenCV WeChat QR.
- ✅ **WebSocket streaming**: Real-time detection with low latency.
- ✅ **REST API**: Static image processing.
- ✅ **Dynamic ROI**: Focus on a Region of Interest for higher accuracy and less bandwidth.
- ✅ **Confidence system**: Consecutive identical detections confirm the barcode to prevent scan flickering.
- ✅ **Backpressure control**: Client-side throttle if the socket output buffer congests.
- ✅ **CORS enabled**: Straightforward frontend calls from any origin.
- ✅ **Health checks**: Simple monitoring endpoints for system availability.

### Supported Formats

#### 1D Barcodes
- EAN-8, EAN-13
- UPC-A, UPC-E
- Code 39, Code 93, Code 128
- ITF (Interleaved 2 of 5)
- Codabar

#### 2D Codes
- QR Code
- Aztec Code
- DataMatrix
- PDF417

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Web Client (HTML5)                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Camera     │  │  WebSocket   │  │  File Upload │      │
│  │   Capture    │  │   Client     │  │   REST API   │      │
│  └───────┬──────┘  └──────┬───────┘  └──────┬───────┘      │
└──────────┼────────────────┼─────────────────┼──────────────┘
           │                │                 │
           ▼                ▼                 ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Server                            │
│  ┌────────────────────────────────────────────────────┐     │
│  │                 Main Application                    │     │
│  │  - CORS Middleware                                  │     │
│  │  - Health Check                                     │     │
│  │  - Redirect Handler                                 │     │
│  └────────┬────────────────────────────┬────────────┬──┘     │
│           │                            │            │        │
│  ┌────────▼────────┐        ┌─────────▼──────┐    │        │
│  │  REST Endpoint  │        │   WebSocket    │    │        │
│  │   /api/v1/image │        │  /api/v1/      │    │        │
│  │                 │        │   realtime/    │    │        │
│  └────────┬────────┘        └─────────┬──────┘    │        │
│           │                           │            │        │
│           └───────────┬───────────────┘            │        │
│                       │                            │        │
│              ┌────────▼────────┐         ┌────────▼──────┐ │
│              │ Image Processing │         │  Test Page    │ │
│              │     Module       │         │   /test       │ │
│              └────────┬─────────┘         └───────────────┘ │
│                       │                                      │
│              ┌────────▼────────┐                            │
│              │  Barcode Utils  │                            │
│              │  - PyZbar       │                            │
│              │  - ZXing-C++    │                            │
│              │  - OpenCV       │                            │
│              └─────────────────┘                            │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

#### REST Mode (Static Image)
```
Client → Upload File → /api/v1/image → process_image() → 
→ Engines (PyZbar/ZXing/OpenCV) → JSON Response → Client
```

#### WebSocket Mode (Real-Time)
```
Client → Capture Frame → ROI Crop → WebSocket Send → 
→ Server Queue → process_image() → WebSocket Response → 
→ Display Results → Next Frame
```

---

## 💻 System Requirements

### Backend (Server)

#### Software
- **Python**: 3.13 or higher
- **uv**: Package manager (recommended)
- **Docker**: 20.10+ (optional, for containerized environments)

#### Python Dependencies
```toml
fastapi[standard]>=0.135.2
opencv-contrib-python-headless>=4.13.0.92
pillow>=12.0.0
pyzbar>=0.1.9
zxing-cpp>=3.0.0
```

#### Linux System Packages
```bash
libzbar0          # For PyZbar
libglib2.0-0      # For OpenCV
libsm6            # For image handling dependencies
libxext6          # X11 extensions
libxrender1       # Rendering support
libgomp1          # OpenMP
libstdc++6        # Standard C++ library
```

#### Recommended Hardware
- **CPU**: 2+ cores (4+ cores recommended)
- **RAM**: 2 GB minimum (4 GB recommended)
- **Network**: 100 Mbps+ bandwidth for smooth video stream frames

### Frontend (Client)

#### Supported Browsers
- ✅ Chrome 90+ (recommended)
- ✅ Firefox 88+
- ✅ Safari 14+ (iOS 14+)
- ✅ Edge 90+
- ⚠️ Opera 76+ (with limitations)

#### Required Web APIs
- **getUserMedia**: Access to camera streams.
- **WebSocket**: Real-time full-duplex communication.
- **Canvas API**: Raw frame capturing and processing.
- **Blob API**: Compressing and formatting images.

#### Permissions
- **Camera**: Essential for real-time streaming scans.
- **HTTPS**: Required in production environments to access browser camera APIs.

---

## ⚙️ Installation and Configuration

### Option 1: Local Development with uv

#### Step 1: Install uv
```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# With pip
pip install uv
```

#### Step 2: Clone the Repository
```bash
git clone https://github.com/Futurion-partners/Omnilector.git
cd Omnilector
```

#### Step 3: Sync Dependencies
```bash
uv sync
```

#### Step 4: Run the Server
```bash
# Development mode (with auto-reload)
uv run omnilector-dev

# Production mode
uv run omnilector
```

The server will start and be available at:
- API Base: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- Web Client: `http://localhost:8000/test`

### Option 2: Docker

#### Build Image
```bash
# Tag with current commit hash
docker build -t omnilector:$(git rev-parse --short HEAD) .

# Tag as latest
docker build -t omnilector:latest .
```

#### Run Container
```bash
# Default port (8000)
docker run --rm -p 8000:8000 omnilector:latest

# Custom port
docker run --rm -e PORT=8080 -p 80:8080 omnilector:latest
```

#### Using Docker Compose
```bash
docker compose up --build
```

### Option 3: Deploy on Dokploy

1. **Link Repository**: Connect your Git repository.
2. **Environment Variables**:
   ```env
   PORT=8000
   BARCODE_ONLY_PYZBAR=1  # Optional: force PyZbar priority
   ```
3. **Build & Deploy**: Dokploy will auto-detect the Dockerfile.
4. **Verification**: Query `/health` to confirm successful deployment.

---

## 📖 Usage Guide

### Mode 1: Web Client (Recommended)

#### Access
Open your browser and go to `http://localhost:8000/test` or `http://localhost:8000/`.

#### Initial Configuration
1. **Resolution**: Select based on code size and quality.
   - `960x720`: Fast, good for small screens.
   - `1280x720`: Optimal balance (recommended).
   - `1920x1080`: High precision, for very small barcodes.

2. **JPEG Quality**: Adjust the slider (0.5 to 0.95).
   - `0.85-0.90`: Recommended default.
   - `0.95`: High quality, larger payload size.
   - `0.70`: Low quality, very fast transfer.

3. **Interval**: Time between captured frames in ms.
   - `800-1000ms`: Rapid scanning.
   - `1200ms`: Balanced default.
   - `1500-2000ms`: Slow network connections.

4. **Advanced Options**:
   - ☑️ **Auto Focus**: Continuously refocus camera (recommended).
   - ☐ **Disable Zoom**: Keeps focal length at 1.0x.
   - ☐ **PNG Mode**: Lossless format, slower but handles distorted codes better.

#### Real-Time Scanning
1. Click **📷 Start Camera**.
2. Grant camera permissions when prompted.
3. Click **🔌 Connect WebSocket**.
4. Point your camera at a barcode.
5. Align the code inside the **green ROI box**.
6. Wait for verification (requires 2 identical consecutive reads).
7. The interface will display the confirmed code and pause.
8. Click **🔍 Scan Another** to resume.

#### Static Image Upload
1. Click **Select file**.
2. Choose an image containing a barcode.
3. The results will display automatically.

### Mode 2: REST API

#### Endpoint: POST /api/v1/image/

**Request**:
```bash
curl -X POST "http://localhost:8000/api/v1/image/" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@barcode_image.jpg"
```

**Response** (JSON):
```json
{
  "ok": true,
  "barcodes": ["1234567890123"],
  "locations": [
    {
      "x": 150,
      "y": 200,
      "width": 300,
      "height": 100
    }
  ],
  "sources": ["pyzbar"]
}
```

#### Python Example
```python
import requests

url = "http://localhost:8000/api/v1/image/"
files = {"file": open("barcode.jpg", "rb")}
response = requests.post(url, files=files)
data = response.json()

if data["ok"]:
    print(f"Detected codes: {data['barcodes']}")
else:
    print("No codes detected")
```

#### JavaScript Example
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/api/v1/image/', {
  method: 'POST',
  body: formData
})
.then(res => res.json())
.then(data => {
  console.log('Codes:', data.barcodes);
})
.catch(err => console.error(err));
```

### Mode 3: WebSocket (Programmatic)

#### Connect
```javascript
const ws = new WebSocket('ws://localhost:8000/api/v1/realtime/');

ws.onopen = () => {
  console.log('Connected');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Result:', data);
};

ws.onerror = (error) => {
  console.error('Error:', error);
};

ws.onclose = () => {
  console.log('Disconnected');
};
```

#### Send Frame
```javascript
// Convert canvas capture to JPEG blob and send
canvas.toBlob((blob) => {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(blob);
  }
}, 'image/jpeg', 0.85);
```

#### Server Response
```json
{
  "type": "result",
  "ok": true,
  "barcodes": ["9780134685991"],
  "locations": [
    {
      "x": 120,
      "y": 180,
      "width": 250,
      "height": 90
    }
  ],
  "sources": ["wechat-qr"]
}
```

---

## 🔌 API Reference

### REST Endpoints

#### POST /api/v1/image/
Processes a static image file and decodes any barcodes found.

- **Method**: POST
- **Content-Type**: `multipart/form-data`
- **Body**:
  - `file` (binary): The image file.

**Response** (200 OK):
```json
{
  "ok": boolean,
  "barcodes": string[],
  "locations": {
    "x": number,
    "y": number,
    "width": number,
    "height": number
  }[],
  "sources": string[]
}
```

#### GET /health
Basic system health check.

**Response** (200 OK):
```json
{
  "status": "ok"
}
```

#### GET /test
Serves the HTML5 web interface.

**Response**: HTML webpage

#### GET /
Redirects to `/test`.

### WebSocket Endpoint

#### WS /api/v1/realtime/
Accepts binary video frames for real-time decoding.

- **Client Message**: Binary (JPEG/PNG blob).
- **Server Message**: JSON text format.

```json
{
  "type": "result" | "ack" | "error",
  "ok": boolean,
  "barcodes": string[],
  "locations": object[],
  "sources": string[],
  "error": string  // Populated only if type="error"
}
```

---

## 🎨 Web Client (Frontend)

The frontend captures camera input using the browser's MediaDevices API and pipelines frames through WebSocket binary messages.

### Main JavaScript Functions

- **`startCamera()`**: Detects and initiates the optimal back camera.
- **`connectWebSocket()`**: Manages WebSocket lifecycle, error handling, and reconnection.
- **`startSendingFrames()`**: Captures frames from the `<video>` element, crops the Region of Interest (ROI), converts the image to JPEG/PNG, and pushes the binary payload.
- **`displayResults()`**: Tracks confidence levels across frames. Employs a debounce lock requiring 2 consecutive reads of the same barcode before confirming the detection.

---

## ⚡ Optimization and Performance

### Backend Optimizations

1. **Downscaling**: Large images are downscaled to a max dimension of 1280px in `utils/image.py` prior to detection, saving significant CPU cycles.
2. **WebSocket Buffering**: Client backpressure checks (`ws.bufferedAmount`) drop frames if the socket buffer exceeds 512KB to avoid latency pileups.

### Recommended Configurations by Scenario

#### High Latency / Cellular Connection
- **Resolution**: 960x720
- **Quality**: 0.70 JPEG
- **Interval**: 2000 ms
- **PNG Mode**: Disabled

#### Low Latency / Wi-Fi
- **Resolution**: 1280x720
- **Quality**: 0.85-0.90 JPEG
- **Interval**: 1000 ms
- **PNG Mode**: Optional

#### Small or Difficult Barcodes
- **Resolution**: 1920x1080
- **Quality**: 0.95 JPEG
- **Interval**: 1500 ms
- **PNG Mode**: Enabled

---

## 🛠️ Troubleshooting

### Common Problems

#### 1. "Camera cannot be accessed"
- **Symptoms**: `NotAllowedError` or camera remains inactive.
- **Fixes**: Check browser permissions, ensure the site runs on HTTPS (required by browsers for camera APIs outside localhost), and shut down other applications using the camera.

#### 2. "WebSocket disconnects frequently"
- **Symptoms**: Scanner halts; console reports connection loss.
- **Fixes**: Verify the backend server is active, ensure client and server are on the same local network, and check firewalls. If bandwidth is choked, increase the frame interval (e.g. to 1500ms).

#### 3. "No codes are detected"
- **Fixes**: Move the barcode into the highlighted green box (ROI), improve lighting, steady the device for 1-2 seconds, or switch to Lossless PNG Mode if the code has poor contrast.

---

## 👨‍💻 Development and Contribution

### Project Structure
```
barcode-python-main/
├── src/
│   └── omnilector/
│       ├── __init__.py              # Entry points
│       ├── main.py                  # Main FastAPI Application
│       ├── models/                  # Pydantic Schemas
│       ├── routes/                  # API Routers (v1)
│       └── utils/                   # Detection & image helpers
├── websocket_test.html              # HTML5 Web client
├── pyproject.toml                   # Project metadata & deps
├── Dockerfile                       # Container definition
├── docker-compose.yml               # Service composition
├── README.md                        # Primary documentation
└── DOCUMENTATION.md                 # This file
```

### Setup Development Environment
```bash
git clone https://github.com/Futurion-partners/Omnilector.git
cd Omnilector
uv sync
uv run omnilector-dev
```

### Running Tests
```bash
# Run all unit tests
pytest

# Check coverage
pytest --cov=src/omnilector
```

---

## 🚀 Production Deployment

### Security Checklist
1. **Enforce HTTPS**: Reverse proxy with Nginx to manage SSL certificates.
2. **CORS Configuration**: Restrict the wildcard `allow_origins=["*"]` to your trusted production domains.
3. **File Validation**: Validate size limits (e.g., max 10MB) and content types (JPEG/PNG/WebP) on image upload endpoints.

**Last update**: October 6, 2025  
**Version**: 1.0.0  
**Author**: Futurion Partners (@Futurion-partners)
