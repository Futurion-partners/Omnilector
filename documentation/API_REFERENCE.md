# 📡 API Reference - Omnilector

## General Information

**Base URL**: `http://localhost:8000`  
**Version**: v1  
**Format**: JSON  
**Authentication**: Not required (in this version)

---

## 🔌 Endpoints

### 1. Health Check

```http
GET /health
```

Verifies the server status.

#### Response (200 OK)

```json
{
  "status": "ok"
}
```

#### Example using curl

```bash
curl http://localhost:8000/health
```

#### Example using Python

```python
import requests

response = requests.get("http://localhost:8000/health")
print(response.json())  # {"status": "ok"}
```

---

### 2. Process Static Image

```http
POST /api/v1/image/
```

Upload an image and receive detected barcodes.

#### Request

**Content-Type**: `multipart/form-data`

**Parameters**:
| Field | Type | Required | Description |
|-------|------|-----------|-------------|
| file  | binary | Yes | Image file (JPEG, PNG, WebP, etc.) |

#### Response (200 OK)

```json
{
  "ok": boolean,
  "barcodes": string[],
  "locations": Array<{
    "x": number,
    "y": number,
    "width": number,
    "height": number
  }>,
  "sources": string[]
}
```

**Fields**:
- `ok`: `true` if codes were detected, `false` otherwise
- `barcodes`: Array of strings containing detected codes
- `locations`: Array of objects with bounding box coordinates for each code
  - `x`: X-coordinate of top-left corner
  - `y`: Y-coordinate of top-left corner
  - `width`: Code width in pixels
  - `height`: Code height in pixels
- `sources`: Array with the detection engine that recognized each code
  - Possible values: `"pyzbar"`, `"zxing-cpp"`, `"wechat-qr"`

#### Example Successful Response

```json
{
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
  "sources": ["pyzbar"]
}
```

#### Example No-Detection Response

```json
{
  "ok": false,
  "barcodes": [],
  "locations": [],
  "sources": []
}
```

#### Error Responses

**400 Bad Request**
```json
{
  "detail": "Invalid file or unsupported format"
}
```

**413 Payload Too Large**
```json
{
  "detail": "File too large"
}
```

**422 Unprocessable Entity**
```json
{
  "detail": [
    {
      "loc": ["body", "file"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**500 Internal Server Error**
```json
{
  "detail": "Internal server error"
}
```

#### Example using curl

```bash
curl -X POST "http://localhost:8000/api/v1/image/" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@barcode.jpg"
```

#### Example using Python (requests)

```python
import requests

url = "http://localhost:8000/api/v1/image/"
files = {"file": open("barcode.jpg", "rb")}

response = requests.post(url, files=files)
data = response.json()

if data["ok"]:
    print(f"Detected codes: {data['barcodes']}")
    print(f"Detected by: {data['sources']}")
else:
    print("No codes detected")
```

#### Example using Python (httpx + asyncio)

```python
import httpx
import asyncio

async def detect_barcode():
    async with httpx.AsyncClient() as client:
        files = {"file": open("barcode.jpg", "rb")}
        response = await client.post(
            "http://localhost:8000/api/v1/image/",
            files=files
        )
        return response.json()

result = asyncio.run(detect_barcode())
print(result)
```

#### Example using JavaScript (fetch)

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/api/v1/image/', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  if (data.ok) {
    console.log('Codes:', data.barcodes);
    console.log('Locations:', data.locations);
  } else {
    console.log('No codes detected');
  }
})
.catch(error => console.error('Error:', error));
```

#### Example using JavaScript (axios)

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const form = new FormData();
form.append('file', fs.createReadStream('barcode.jpg'));

axios.post('http://localhost:8000/api/v1/image/', form, {
  headers: form.getHeaders()
})
.then(response => {
  console.log('Result:', response.data);
})
.catch(error => {
  console.error('Error:', error.message);
});
```

---

### 3. Real-Time WebSocket

```
WS /api/v1/realtime/
```

Establishes a WebSocket connection for real-time streaming detection.

#### Communication Protocol

**1. Client Connects**
```javascript
const ws = new WebSocket('ws://localhost:8000/api/v1/realtime/');
```

**2. Server Accepts Connection**
- State: `WebSocket.OPEN` (readyState = 1)

**3. Client Sends Frames**
- Type: **Binary** (Blob or ArrayBuffer)
- Format: JPEG or PNG
- Recommended rate: 1 frame every 800-1500ms

**4. Server Processes and Responds**
- Type: **Text** (JSON string)
- Format: See message structures below

#### Server Message Types

##### A. Detection Result

```json
{
  "type": "result",
  "ok": boolean,
  "barcodes": string[],
  "locations": Array<{
    "x": number,
    "y": number,
    "width": number,
    "height": number
  }>,
  "sources": string[]
}
```

**Example with detection**:
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
  "sources": ["pyzbar"]
}
```

**Example without detection**:
```json
{
  "type": "result",
  "ok": false,
  "barcodes": [],
  "locations": [],
  "sources": []
}
```

##### B. Acknowledgement (ACK)

Response to text messages sent by the client.

```json
{
  "type": "ack",
  "message": "Text messages not supported"
}
```

##### C. Error

```json
{
  "type": "error",
  "error": "Error description"
}
```

**Example**:
```json
{
  "type": "error",
  "error": "Invalid image format"
}
```

#### Complete JavaScript Example

```javascript
const ws = new WebSocket('ws://localhost:8000/api/v1/realtime/');

// Connection established
ws.onopen = () => {
  console.log('✅ WebSocket connected');
  startSendingFrames();
};

// Message received from server
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  switch(data.type) {
    case 'result':
      if (data.ok) {
        console.log('Detected codes:', data.barcodes);
        console.log('Locations:', data.locations);
        console.log('Detected by:', data.sources);
      } else {
        console.log('No detections in this frame');
      }
      break;
      
    case 'error':
      console.error('Server error:', data.error);
      break;
      
    case 'ack':
      console.log('ACK:', data.message);
      break;
  }
};

// Connection closed
ws.onclose = () => {
  console.log('❌ WebSocket disconnected');
};

// Connection error
ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

// Function to capture and send frames
function startSendingFrames() {
  const video = document.getElementById('video');
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  
  setInterval(() => {
    if (ws.readyState !== WebSocket.OPEN) return;
    
    // Capture frame from video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0);
    
    // Convert to blob and send
    canvas.toBlob((blob) => {
      if (blob && ws.readyState === WebSocket.OPEN) {
        ws.send(blob);
      }
    }, 'image/jpeg', 0.85);
  }, 1000);  // 1 frame per second
}
```

#### Example using Python (websockets)

```python
import asyncio
import websockets
import cv2
import json

async def detect_realtime():
    uri = "ws://localhost:8000/api/v1/realtime/"
    
    async with websockets.connect(uri) as websocket:
        print("✅ Connected")
        
        # Capture video from webcam
        cap = cv2.VideoCapture(0)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Encode frame as JPEG
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            
            # Send binary data
            await websocket.send(buffer.tobytes())
            
            # Receive response
            response = await websocket.recv()
            data = json.loads(response)
            
            if data.get("ok"):
                print(f"Codes: {data['barcodes']}")
            
            # Wait 1 second
            await asyncio.sleep(1)
        
        cap.release()

asyncio.run(detect_realtime())
```

#### Best Practices

1. **Backpressure Control**: Check `ws.bufferedAmount` before sending frames
   ```javascript
   if (ws.bufferedAmount > 512 * 1024) {
     console.log('Buffer full, skipping frame');
     return;
   }
   ```

2. **Frame Rate**: Avoid sending more than 2-3 frames per second
   ```javascript
   const FRAME_INTERVAL = 1000; // 1 second
   ```

3. **Image Quality**: Use JPEG with quality 0.80-0.90 to balance bandwidth and accuracy
   ```javascript
   canvas.toBlob(blob => ws.send(blob), 'image/jpeg', 0.85);
   ```

4. **Reconnection Logic**:
   ```javascript
   ws.onclose = () => {
     setTimeout(() => {
       console.log('Reconnecting...');
       connectWebSocket();
     }, 2000);
   };
   ```

5. **Timeout**: Implement client-side timeouts for silent connections
   ```javascript
   let lastResponseTime = Date.now();
   
   ws.onmessage = () => {
     lastResponseTime = Date.now();
   };
   
   setInterval(() => {
     if (Date.now() - lastResponseTime > 5000) {
        console.warn('No response in 5 seconds, closing socket');
        ws.close();
     }
   }, 1000);
   ```

---

### 4. Interactive Documentation (Swagger)

```http
GET /docs
```

Interactive web UI to test and explore the API.

#### Features
- 📖 Complete endpoint documentation
- 🧪 Execute endpoints directly from the browser
- 📋 Request/Response examples
- 🔍 Data schemas validation

#### Access
```
http://localhost:8000/docs
```

---

### 5. ReDoc (Alternative UI)

```http
GET /redoc
```

Alternative API documentation formatted with ReDoc layout.

#### Access
```
http://localhost:8000/redoc
```

---

## 📊 HTTP Status Codes

| Code | Label | Trigger |
|------|-------|---------|
| 200 | OK | Request processed successfully |
| 400 | Bad Request | Invalid file type or incorrect parameters |
| 404 | Not Found | Endpoint does not exist |
| 413 | Payload Too Large | File size exceeds limit (>10MB) |
| 422 | Unprocessable Entity | Parameter validation failed |
| 500 | Internal Server Error | Server-side execution error |

---

## 🔐 CORS (Cross-Origin Resource Sharing)

The API is configured to accept CORS requests from all origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
```

**Implications**:
- ✅ You can invoke the API directly from any client-side website.
- ✅ No special headers setup is required on the client side.
- ⚠️ In production, consider restricting `allow_origins` to trusted domains.

---

## 🚀 Rate Limiting

**Current State**: Not implemented at application level.

**Production Recommendations**:
- Suggested REST API rate limit: 100 requests/minute per IP.
- WebSocket limit: Maximum of 10 simultaneous connections per IP.

---

## 📝 Data Types

### BarcodeResponse

```typescript
interface BarcodeResponse {
  ok: boolean;
  barcodes: string[];
  locations: Location[];
  sources: string[];
}
```

### Location

```typescript
interface Location {
  x: number;        // X coordinate of top-left corner
  y: number;        // Y coordinate of top-left corner
  width: number;    // Width in pixels
  height: number;   // Height in pixels
}
```

### WebSocketMessage

```typescript
type WebSocketMessage = 
  | WebSocketResult
  | WebSocketAck
  | WebSocketError;

interface WebSocketResult {
  type: "result";
  ok: boolean;
  barcodes: string[];
  locations: Location[];
  sources: string[];
}

interface WebSocketAck {
  type: "ack";
  message: string;
}

interface WebSocketError {
  type: "error";
  error: string;
}
```

---

## 🧪 Testing

### Example Test using pytest

```python
from fastapi.testclient import TestClient
from omnilector.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_image_detection():
    with open("test_barcode.jpg", "rb") as f:
        response = client.post(
            "/api/v1/image/",
            files={"file": ("test.jpg", f, "image/jpeg")}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "ok" in data
    assert "barcodes" in data

def test_websocket():
    with client.websocket_connect("/api/v1/realtime/") as ws:
        # Send a sample test frame
        with open("test_frame.jpg", "rb") as f:
            ws.send_bytes(f.read())
        
        # Receive result
        data = ws.receive_json()
        assert data["type"] == "result"
```

---

## 📚 Additional Resources

- **OpenAPI Spec**: http://localhost:8000/openapi.json
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc UI**: http://localhost:8000/redoc

---

## 🆘 Support

To report bugs or request features:
- **GitHub Issues**: [github.com/Futurion-partners/Omnilector/issues](https://github.com/Futurion-partners/Omnilector/issues)
- **Email**: support@futurion.com

---

**Last update**: October 6, 2025  
**API Version**: v1  
**Document Version**: 1.0.0
