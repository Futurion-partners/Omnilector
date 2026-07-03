# 📷 Omnilector - Barcode & QR Code Detection API

Process various types of barcodes and QR codes with ease. This API offers static image processing via REST and real-time detection through WebSockets.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.13+-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116+-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

## ✨ Key Features

- 🔍 **Multi-engine detection**: PyZbar, ZXing-C++, and OpenCV WeChat QR.
- 📡 **WebSocket streaming**: Real-time detection with low latency.
- 🖼️ **REST API**: Static image processing.
- 🎯 **Dynamic ROI**: Focus on a Region of Interest for higher accuracy.
- ✅ **Confidence system**: Confirmation of detected codes over consecutive frames.
- 🐳 **Docker ready**: Containerization ready.
- 📚 **Full documentation**: Integrated Swagger UI.

## 📋 Supported Formats

### 1D Barcodes
EAN-8, EAN-13, UPC-A, UPC-E, Code 39, Code 93, Code 128, ITF, Codabar

### 2D Codes
QR Code, Aztec Code, DataMatrix, PDF417

---

## 🚀 Quick Start

```bash
# 1. Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clone the project
git clone https://github.com/Futurion-partners/Omnilector.git
cd Omnilector

# 3. Install dependencies
uv sync

# 4. Run the server
uv run omnilector-dev

# 5. Open browser
# http://localhost:8000
```

See **[QUICKSTART.md](documentation/QUICKSTART.md)** for detailed instructions.

---

## 📚 Full Documentation

| Document | Description |
|-----------|-------------|
| **[QUICKSTART.md](documentation/QUICKSTART.md)** | ⏱️ 5-minute start guide |
| **[DOCUMENTATION.md](documentation/DOCUMENTATION.md)** | 📖 Full technical documentation |
| **[API_REFERENCE.md](documentation/API_REFERENCE.md)** | 📡 REST and WebSocket API Reference |
| **[FRONTEND_GUIDE.md](documentation/FRONTEND_GUIDE.md)** | 🎨 JavaScript Web Client Guide |

---

## 📋 Table of Contents

- [Omnilector](#omnilector)
  - [Quick Start](#quick-start)
  - [Full Documentation](#full-documentation)
  - [Table of Contents](#table-of-contents)
  - [Run and Configure the Project](#run-and-configure-the-project)
    - [With Docker](#with-docker)
      - [Build the Docker Image](#build-the-docker-image)
      - [Run the API](#run-the-api)
        - [Modify Ports](#modify-ports)
    - [Local Development](#local-development)
      - [Local Configuration](#local-configuration)
      - [Run Locally](#run-locally)
        - [Reload Enabled](#reload-enabled)
        - [Reload Disabled](#reload-disabled)

---

## 🎯 Basic Usage

### Web Interface (Recommended)

1. Start the server: `uv run omnilector-dev`
2. Open http://localhost:8000 in your browser.
3. Click "📷 Start Camera".
4. Click "🔌 Connect WebSocket".
5. Point your camera at a barcode.

### REST API

```bash
curl -X POST "http://localhost:8000/api/v1/image/" \
  -F "file=@barcode.jpg"
```

### Python

```python
import requests

url = "http://localhost:8000/api/v1/image/"
files = {"file": open("barcode.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

See **[API_REFERENCE.md](documentation/API_REFERENCE.md)** for more examples.

---

## 🛠️ Run and Configure the Project

### With Docker

You may want to regenerate the `.dockerignore` file if you have modified `.gitignore` or `.prodignore`. You can do so by running the following command:

> [!NOTE]
> This command will overwrite the `.dockerignore` file with the entire contents of the `.gitignore` and `.prodignore` files.

```sh
cat .gitignore .prodignore > .dockerignore
```

#### Build the Docker Image

```sh
docker build -t omnilector:$(git rev-parse --short HEAD) . # Tag with current commit hash
docker build -t omnilector:latest . # Tag as latest
```

#### Run the API

Once you have [built](#build-the-docker-image) the image, run:

```sh
docker run --rm -p 8000:8000 omnilector:latest
```

Now you can visit the [generated documentation](http://127.0.0.1:8000/docs) and check out the API.

##### Modify Ports

You can configure the port by setting the `PORT` environment variable to the desired port number.

By default, it is set to `8000`. If you want to change the internal port, you can run the following command, which sets the internal port to `8080` and maps port `80` of the host to port `8080` of the container.

```bash
docker run --rm -e PORT=8080 -p 80:8080 omnilector:latest
```

The API should now be accessible at [http://127.0.0.1:80/docs](http://127.0.0.1:80/docs).

##### Using docker-compose

Alternatively, you can use docker-compose to build and run the services:

```bash
docker compose up --build
```

This exposes the service on http://localhost:8000 and includes a health check.

---

## 📡 Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Redirects to `/test` |
| `/test` | GET | Web test client |
| `/docs` | GET | Interactive Swagger UI documentation |
| `/health` | GET | Health check status |
| `/api/v1/image/` | POST | Process static image |
| `/api/v1/realtime/` | WebSocket | Real-time detection |

---

## 🐳 Deployment on Dokploy

To deploy on [Dokploy](https://dokploy.com/) (a self-hosted PaaS):

1. **Build and Deploy**: Push your code to your Git repository. Dokploy will build using either the Dockerfile or pyproject.toml.
2. **Dependencies**: Ensure all dependencies are listed in `pyproject.toml`. If you encounter a `ModuleNotFoundError`, check build logs and redeploy after adding the missing packages (e.g., `pillow` was added for image processing).
3. **Environment Variables**:
   - Set `BARCODE_ONLY_PYZBAR=1` to prioritize PyZbar (default).
   - Adjust `PORT` if needed (defaults to 8000).
4. **Troubleshooting**:
   - **Missing Modules**: If build fails due to import errors, add the missing package to `pyproject.toml` dependencies and redeploy.
   - **Version Verification**: After deploying, visit `/api/v1/version` to confirm that the app started successfully and check the version.
   - **Logs**: Check Dokploy logs for errors like "No module named 'PIL'". This indicates Pillow is not installed; add `pillow>=12.0.0` to dependencies.
   - **Redeploy**: Force a rebuild by pushing a new commit or trigger a manual build in Dokploy.
   - **Health Check**: The app includes a health check endpoint at `/health` (if configured in the Dockerfile).

### Local Development

> [!TIP]
> If you are not familiar with [uv](https://docs.astral.sh/uv/), you can watch [this video](https://youtu.be/AMdG7IjgSPM).

#### Local Configuration

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) if it is not already present on your machine.
2. Synchronize the required packages:
    ```sh
    uv sync
    ```

And you are good to go!

#### Run Locally

To run the following commands, you must first [configure the project locally](#local-configuration) and ensure your packages are synced.

##### Reload Enabled

This will automatically reload the API instance once a file is updated:

```sh
uv run omnilector-dev
```

##### Reload Disabled

This runs the API with the current state of the project and will **not** reload on code modifications:

```sh
uv run omnilector
```

---

## 🧪 Testing

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=src/omnilector

# Run integration tests
pytest tests/integration/
```

---

## 🤝 Contributing

Please refer to our **[Contributing Guide (CONTRIBUTING.md)](CONTRIBUTING.md)** for details on the process for submitting contributions to the project.

---

## 📊 Performance

- **REST API Latency**: ~50-80 ms per image
- **WebSocket Latency**: ~100-150 ms total
- **Throughput**: ~10-15 detections/second per connection
- **Detection Rate**: 95-98% for common codes

---

## 🔧 Environment Variables

```env
PORT=8000                    # Server port
HOST=0.0.0.0                 # Server host
LOG_LEVEL=info               # Logging level
BARCODE_ONLY_PYZBAR=0        # Only use PyZbar (1=yes, 0=no)
```

---

## 🆘 Troubleshooting

### Codes are not detected
- ✅ Verify the code is within the green ROI box.
- ✅ Improve the lighting.
- ✅ Increase JPEG quality to 0.90-0.95.
- ✅ Enable "Lossless PNG Mode".

### Camera does not work
- ✅ Grant camera permissions in the browser.
- ✅ Use HTTPS in production (localhost works with HTTP).
- ✅ Close other apps that might be using the camera.

See **[DOCUMENTATION.md](documentation/DOCUMENTATION.md)** "Troubleshooting" section for more cases.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👥 Authors

- **Futurion Partners** - [@Futurion-partners](https://github.com/Futurion-partners)

---

## 📞 Support

- **GitHub Issues**: [github.com/Futurion-partners/Omnilector/issues](https://github.com/Futurion-partners/Omnilector/issues)
- **Email**: support@futurion.com
