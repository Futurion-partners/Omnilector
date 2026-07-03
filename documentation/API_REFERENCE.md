# 📡 API Reference - Futurion Barcode

## Información General

**Base URL**: `http://localhost:8000`  
**Versión**: v1  
**Formato**: JSON  
**Autenticación**: No requerida (en esta versión)

---

## 🔌 Endpoints

### 1. Health Check

```http
GET /health
```

Verifica el estado del servidor.

#### Response (200 OK)

```json
{
  "status": "ok"
}
```

#### Ejemplo con curl

```bash
curl http://localhost:8000/health
```

#### Ejemplo con Python

```python
import requests

response = requests.get("http://localhost:8000/health")
print(response.json())  # {"status": "ok"}
```

---

### 2. Procesar Imagen Estática

```http
POST /api/v1/image/
```

Envía una imagen y recibe los códigos de barras detectados.

#### Request

**Content-Type**: `multipart/form-data`

**Parameters**:
| Campo | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| file  | binary | Sí | Archivo de imagen (JPEG, PNG, WebP, etc.) |

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

**Campos**:
- `ok`: `true` si se detectaron códigos, `false` si no
- `barcodes`: Array de strings con los códigos detectados
- `locations`: Array de objetos con las coordenadas de cada código
  - `x`: Coordenada X del borde superior izquierdo
  - `y`: Coordenada Y del borde superior izquierdo
  - `width`: Ancho del código en píxeles
  - `height`: Alto del código en píxeles
- `sources`: Array con el motor que detectó cada código
  - Valores posibles: `"pyzbar"`, `"zxing-cpp"`, `"wechat-qr"`

#### Ejemplo de Respuesta Exitosa

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

#### Ejemplo de Respuesta sin Detección

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
  "detail": "Archivo inválido o formato no soportado"
}
```

**413 Payload Too Large**
```json
{
  "detail": "Archivo demasiado grande"
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
  "detail": "Error interno del servidor"
}
```

#### Ejemplo con curl

```bash
curl -X POST "http://localhost:8000/api/v1/image/" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@barcode.jpg"
```

#### Ejemplo con Python (requests)

```python
import requests

url = "http://localhost:8000/api/v1/image/"
files = {"file": open("barcode.jpg", "rb")}

response = requests.post(url, files=files)
data = response.json()

if data["ok"]:
    print(f"Códigos detectados: {data['barcodes']}")
    print(f"Detectado con: {data['sources']}")
else:
    print("No se detectaron códigos")
```

#### Ejemplo con Python (httpx + asyncio)

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

#### Ejemplo con JavaScript (fetch)

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
    console.log('Códigos:', data.barcodes);
    console.log('Ubicaciones:', data.locations);
  } else {
    console.log('No se detectaron códigos');
  }
})
.catch(error => console.error('Error:', error));
```

#### Ejemplo con JavaScript (axios)

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
  console.log('Resultado:', response.data);
})
.catch(error => {
  console.error('Error:', error.message);
});
```

---

### 3. WebSocket en Tiempo Real

```
WS /api/v1/realtime/
```

Establece una conexión WebSocket para detección en tiempo real.

#### Protocolo de Comunicación

**1. Cliente se conecta**
```javascript
const ws = new WebSocket('ws://localhost:8000/api/v1/realtime/');
```

**2. Servidor acepta conexión**
- Estado: `WebSocket.OPEN` (readyState = 1)

**3. Cliente envía frames**
- Tipo: **Binary** (Blob o ArrayBuffer)
- Formato: JPEG o PNG
- Frecuencia recomendada: 1 frame cada 800-1500ms

**4. Servidor procesa y responde**
- Tipo: **Text** (JSON string)
- Formato: Ver estructura de mensajes abajo

#### Tipos de Mensajes del Servidor

##### A. Resultado de Detección

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

**Ejemplo con detección**:
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

**Ejemplo sin detección**:
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

Respuesta a mensajes de texto del cliente.

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
  "error": "Descripción del error"
}
```

**Ejemplo**:
```json
{
  "type": "error",
  "error": "Invalid image format"
}
```

#### Ejemplo Completo con JavaScript

```javascript
const ws = new WebSocket('ws://localhost:8000/api/v1/realtime/');

// Conexión establecida
ws.onopen = () => {
  console.log('✅ WebSocket conectado');
  startSendingFrames();
};

// Mensaje recibido del servidor
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  switch(data.type) {
    case 'result':
      if (data.ok) {
        console.log('Códigos detectados:', data.barcodes);
        console.log('Ubicaciones:', data.locations);
        console.log('Detectado con:', data.sources);
      } else {
        console.log('Sin detecciones en este frame');
      }
      break;
      
    case 'error':
      console.error('Error del servidor:', data.error);
      break;
      
    case 'ack':
      console.log('ACK:', data.message);
      break;
  }
};

// Conexión cerrada
ws.onclose = () => {
  console.log('❌ WebSocket desconectado');
};

// Error en la conexión
ws.onerror = (error) => {
  console.error('Error en WebSocket:', error);
};

// Función para enviar frames
function startSendingFrames() {
  const video = document.getElementById('video');
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  
  setInterval(() => {
    if (ws.readyState !== WebSocket.OPEN) return;
    
    // Capturar frame del video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0);
    
    // Convertir a blob y enviar
    canvas.toBlob((blob) => {
      if (blob && ws.readyState === WebSocket.OPEN) {
        ws.send(blob);
      }
    }, 'image/jpeg', 0.85);
  }, 1000);  // 1 frame por segundo
}
```

#### Ejemplo con Python (websockets)

```python
import asyncio
import websockets
import cv2

async def detect_realtime():
    uri = "ws://localhost:8000/api/v1/realtime/"
    
    async with websockets.connect(uri) as websocket:
        print("✅ Conectado")
        
        # Capturar video
        cap = cv2.VideoCapture(0)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Codificar frame a JPEG
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            
            # Enviar
            await websocket.send(buffer.tobytes())
            
            # Recibir respuesta
            response = await websocket.recv()
            data = json.loads(response)
            
            if data.get("ok"):
                print(f"Códigos: {data['barcodes']}")
            
            # Esperar 1 segundo
            await asyncio.sleep(1)
        
        cap.release()

asyncio.run(detect_realtime())
```

#### Mejores Prácticas

1. **Backpressure Control**: Verifica `ws.bufferedAmount` antes de enviar
   ```javascript
   if (ws.bufferedAmount > 512 * 1024) {
     console.log('Buffer lleno, saltando frame');
     return;
   }
   ```

2. **Frame Rate**: No envíes más de 2-3 frames por segundo
   ```javascript
   const FRAME_INTERVAL = 1000; // 1 segundo
   ```

3. **Calidad de Imagen**: Usa JPEG con calidad 0.80-0.90
   ```javascript
   canvas.toBlob(blob => ws.send(blob), 'image/jpeg', 0.85);
   ```

4. **Manejo de Reconexión**:
   ```javascript
   ws.onclose = () => {
     setTimeout(() => {
       console.log('Reintentando conexión...');
       connectWebSocket();
     }, 2000);
   };
   ```

5. **Timeout**: Establece un timeout para frames sin respuesta
   ```javascript
   let lastResponseTime = Date.now();
   
   ws.onmessage = () => {
     lastResponseTime = Date.now();
   };
   
   setInterval(() => {
     if (Date.now() - lastResponseTime > 5000) {
       console.warn('Sin respuesta en 5 segundos');
       ws.close();
     }
   }, 1000);
   ```

---

### 4. Documentación Interactiva (Swagger)

```http
GET /docs
```

Interfaz web interactiva para probar la API.

#### Características

- 📖 Documentación completa de endpoints
- 🧪 Probar endpoints directamente desde el navegador
- 📋 Ejemplos de request/response
- 🔍 Schemas de datos

#### Acceso

```
http://localhost:8000/docs
```

---

### 5. ReDoc (Documentación Alternativa)

```http
GET /redoc
```

Documentación en formato ReDoc (más legible).

#### Acceso

```
http://localhost:8000/redoc
```

---

## 📊 Códigos de Estado HTTP

| Código | Significado | Cuándo ocurre |
|--------|-------------|---------------|
| 200 | OK | Solicitud procesada correctamente |
| 400 | Bad Request | Archivo inválido o parámetros incorrectos |
| 404 | Not Found | Endpoint no existe |
| 413 | Payload Too Large | Archivo demasiado grande (>10MB) |
| 422 | Unprocessable Entity | Validación de parámetros falló |
| 500 | Internal Server Error | Error interno del servidor |

---

## 🔐 CORS (Cross-Origin Resource Sharing)

La API tiene CORS habilitado para todos los orígenes:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
```

**Implicaciones**:
- ✅ Puedes llamar la API desde cualquier origen
- ✅ No necesitas configuración especial en el cliente
- ⚠️ En producción, considera restringir `allow_origins`

---

## 🚀 Rate Limiting

**Estado actual**: No implementado

**Recomendación para producción**:
- Límite sugerido: 100 requests/minuto por IP
- WebSocket: Máximo 10 conexiones simultáneas por IP

---

## 📝 Tipos de Datos

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
  x: number;        // Coordenada X
  y: number;        // Coordenada Y
  width: number;    // Ancho en píxeles
  height: number;   // Alto en píxeles
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

### Ejemplo de Test con pytest

```python
from fastapi.testclient import TestClient
from futurion_barcode.main import app

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
        # Enviar frame de prueba
        with open("test_frame.jpg", "rb") as f:
            ws.send_bytes(f.read())
        
        # Recibir respuesta
        data = ws.receive_json()
        assert data["type"] == "result"
```

---

## 📚 Recursos Adicionales

- **OpenAPI Spec**: http://localhost:8000/openapi.json
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🆘 Soporte

Para reportar bugs o solicitar features:
- **GitHub Issues**: [github.com/Futurion-partners/barcode-2/issues](https://github.com/Futurion-partners/barcode-2/issues)
- **Email**: support@futurion.com

---

**Última actualización**: Octubre 6, 2025  
**Versión API**: v1  
**Versión Documento**: 1.0.0
