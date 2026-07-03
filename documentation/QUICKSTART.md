# Quick Start Guide

### Step 1: Install uv (Package Manager)

**Windows (PowerShell)**:
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux/macOS**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 2: Clone the Project

```bash
git clone https://github.com/Futurion-partners/Omnilector.git
cd Omnilector
```

### Step 3: Install Dependencies

```bash
uv sync
```

### Step 4: Run the Server

```bash
uv run omnilector-dev
```

### Step 5: Open the Web Client

Open your browser at: **http://localhost:8000**

---

## 🎯 Basic Usage

### Option A: Real-Time Scanning

1. **Start Camera** → Click 📷 "Start Camera"
2. **Allow access** → Grant camera access when requested by the browser
3. **Connect WebSocket** → Click 🔌 "Connect WebSocket"
4. **Scan** → Point your camera at a barcode or QR code
5. **Keep focused** → Keep the barcode within the green Region of Interest (ROI) box
6. **Confirmation** → Wait for confirmation (requires 2 consecutive identical detections)
7. **Result** → The detected code will appear on screen with a green background
8. **Next scan** → Click "🔍 Scan Another"

### Option B: Upload Image

1. **Select file** → Click the file selection button
2. **Choose image** → Select a photo containing barcodes
3. **View result** → The detected code will be displayed automatically

---

## ⚙️ Recommended Configuration

### For Standard Barcodes
- **Resolution**: 1280x720
- **JPEG Quality**: 0.85
- **Interval**: 1200 ms

### For Small or Challenging Barcodes
- **Resolution**: 1920x1080
- **JPEG Quality**: 0.95
- **Interval**: 1500 ms
- **Enable**: ☑️ Lossless PNG Mode

### For Slow Connections
- **Resolution**: 960x720
- **JPEG Quality**: 0.70
- **Interval**: 2000 ms

---

## 🐳 Alternative with Docker

### Build and Run

```bash
docker build -t omnilector:latest .
docker run --rm -p 8000:8000 omnilector:latest
```

### With Docker Compose

```bash
docker compose up --build
```

Access at: **http://localhost:8000**

---

## 🔗 Main Endpoints

### Web Interface
- **http://localhost:8000** - Redirects to /test
- **http://localhost:8000/test** - Complete web client test page

### REST API
- **POST http://localhost:8000/api/v1/image/** - Process static image

### WebSocket
- **ws://localhost:8000/api/v1/realtime/** - Real-time connection endpoint

### Utilities
- **http://localhost:8000/docs** - Interactive Swagger UI documentation
- **http://localhost:8000/health** - Health check endpoint

---

## 📱 Usage from Mobile

### On the Same Wi-Fi Network

1. **Find your local IP**:
   
   **Windows**:
   ```powershell
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., 192.168.1.100)
   
   **Linux/macOS**:
   ```bash
   ifconfig | grep "inet "
   ```

2. **Access from your mobile device**:
   ```
   http://192.168.1.100:8000
   ```
   (Replace with your actual local IP address)

3. **Allow camera access** when prompted by your mobile browser.

---

## 🧪 Testing the API with curl

### Upload an Image

```bash
curl -X POST "http://localhost:8000/api/v1/image/" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@my_code.jpg"
```

### Expected Response

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

---

## 🔍 Verifying Everything Works

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Should return: `{"status":"ok"}`

### 2. Verify Server Logs

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### 3. Open in Browser

Go to http://localhost:8000 and verify the interface loads correctly.

---

## ❌ Quick Troubleshooting

### "I cannot access the camera"
- ✅ Check browser permissions (camera icon in the address bar).
- ✅ Use HTTPS in production (localhost works fine with HTTP).
- ✅ Close other apps that may be using the camera.
- ✅ **Alternative**: Use the "Upload Image" option instead.

### "WebSocket does not connect"
- ✅ Verify the server is running.
- ✅ Ensure no firewall is blocking port 8000.
- ✅ If on a local network, double-check your IP address.

### "No codes are detected"
- ✅ Ensure the code is inside the **green ROI box**.
- ✅ Improve the lighting.
- ✅ Keep the camera steady for 1-2 seconds.
- ✅ Increase JPEG quality to 0.90-0.95.
- ✅ Enable "Lossless PNG Mode".

### "ModuleNotFoundError"
```bash
uv sync  # Reinstall dependencies
```

---

## 📚 Complete Documentation

For more details, see:
- **DOCUMENTATION.md** - Comprehensive project documentation
- **FRONTEND_GUIDE.md** - Detailed web client guide
- **README.md** - Technical quick reference

---

## 🆘 Support

- **GitHub Issues**: [github.com/Futurion-partners/Omnilector/issues](https://github.com/Futurion-partners/Omnilector/issues)
- **Email**: support@futurion.com

---

## 🎉 Ready!

You are all set. Try scanning:
- Product barcodes (EAN/UPC)
- QR codes from websites
- Codes on printed documents

**Tip**: For best results, keep the code centered in the green box and hold steady for 1-2 seconds.
