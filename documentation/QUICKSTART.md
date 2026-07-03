#  Guía de Inicio Rápido 


### Paso 1: Instalar uv (Gestor de Paquetes)

**Windows (PowerShell)**:
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux/macOS**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Paso 2: Clonar el Proyecto

```bash
git clone https://github.com/Futurion-partners/Omnilector.git
cd Omnilector
```

### Paso 3: Instalar Dependencias

```bash
uv sync
```

### Paso 4: Ejecutar el Servidor

```bash
uv run omnilector-dev
```

### Paso 5: Abrir el Cliente Web

Abre tu navegador en: **http://localhost:8000**

---

## 🎯 Uso Básico

### Opción A: Escaneo en Tiempo Real

1. **Iniciar Cámara** → Haz clic en 📷 "Iniciar Cámara"
2. **Permitir acceso** → Autoriza el acceso a la cámara cuando el navegador lo solicite
3. **Conectar WebSocket** → Haz clic en 🔌 "Conectar WebSocket"
4. **Escanear** → Apunta tu cámara al código de barras
5. **Mantén enfocado** → Mantén el código dentro del recuadro verde
6. **Confirmación** → Espera la confirmación (2 detecciones consecutivas)
7. **Resultado** → El código aparecerá en pantalla con fondo verde
8. **Siguiente código** → Haz clic en "🔍 Escanear Otro"

### Opción B: Subir Imagen

1. **Seleccionar archivo** → Haz clic en el botón de selección de archivo
2. **Elegir imagen** → Selecciona una foto con códigos de barras
3. **Ver resultado** → El código se mostrará automáticamente

---

## ⚙️ Configuración Recomendada

### Para Códigos Normales
- **Resolución**: 1280x720
- **Calidad JPEG**: 0.85
- **Intervalo**: 1200 ms

### Para Códigos Pequeños o Difíciles
- **Resolución**: 1920x1080
- **Calidad JPEG**: 0.95
- **Intervalo**: 1500 ms
- **Activar**: ☑️ Modo PNG sin pérdida

### Para Conexiones Lentas
- **Resolución**: 960x720
- **Calidad JPEG**: 0.70
- **Intervalo**: 2000 ms

---

## 🐳 Alternativa con Docker

### Construir y Ejecutar

```bash
docker build -t omnilector:latest .
docker run --rm -p 8000:8000 omnilector:latest
```

### Con Docker Compose

```bash
docker compose up --build
```

Accede a: **http://localhost:8000**

---

## 🔗 Endpoints Principales

### Interfaz Web
- **http://localhost:8000** - Redirige a /test
- **http://localhost:8000/test** - Cliente web completo

### API REST
- **POST http://localhost:8000/api/v1/image/** - Procesar imagen estática

### WebSocket
- **ws://localhost:8000/api/v1/realtime/** - Conexión en tiempo real

### Utilidades
- **http://localhost:8000/docs** - Documentación interactiva (Swagger)
- **http://localhost:8000/health** - Health check

---

## 📱 Uso desde Móvil

### En la Misma Red WiFi

1. **Encuentra tu IP local**:
   
   **Windows**:
   ```powershell
   ipconfig
   ```
   Busca "IPv4 Address" (ej: 192.168.1.100)
   
   **Linux/macOS**:
   ```bash
   ifconfig | grep "inet "
   ```

2. **Accede desde tu móvil**:
   ```
   http://192.168.1.100:8000
   ```
   (Reemplaza con tu IP)

3. **Permite acceso a la cámara** cuando el navegador lo solicite

---

## 🧪 Probar la API con curl

### Subir una Imagen

```bash
curl -X POST "http://localhost:8000/api/v1/image/" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@mi_codigo.jpg"
```

### Respuesta Esperada

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

## 🔍 Verificar que Todo Funciona

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Debe retornar: `{"status":"ok"}`

### 2. Verificar Logs del Servidor

Deberías ver:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### 3. Abrir en Navegador

Ve a http://localhost:8000 y verifica que cargue la interfaz.

---

## ❌ Solución Rápida de Problemas

### "No puedo acceder a la cámara"
- ✅ Verifica permisos del navegador (ícono de cámara en barra de direcciones)
- ✅ Usa HTTPS en producción (localhost funciona con HTTP)
- ✅ Cierra otras apps que usen la cámara
- ✅ **Alternativa**: Usa la opción de subir archivo

### "WebSocket no conecta"
- ✅ Verifica que el servidor esté corriendo
- ✅ Revisa que no haya firewall bloqueando el puerto 8000
- ✅ Si estás en red local, usa la IP correcta

### "No se detectan códigos"
- ✅ Asegúrate de que el código esté dentro del **recuadro verde**
- ✅ Mejora la iluminación
- ✅ Mantén la cámara estable 1-2 segundos
- ✅ Aumenta la calidad JPEG a 0.90-0.95
- ✅ Activa "Modo PNG sin pérdida"

### "ModuleNotFoundError"
```bash
uv sync  # Reinstalar dependencias
```

---

## 📚 Documentación Completa

Para más detalles, consulta:
- **DOCUMENTATION.md** - Documentación completa del proyecto
- **FRONTEND_GUIDE.md** - Guía detallada del cliente web
- **README.md** - Documentación técnica

---

## 🆘 Soporte

- **GitHub Issues**: [github.com/Futurion-partners/Omnilector/issues](https://github.com/Futurion-partners/Omnilector/issues)
- **Email**: support@futurion.com

---

## 🎉 ¡Listo!

Ya tienes todo configurado. Prueba escaneando:
- Códigos de barras de productos
- Códigos QR de sitios web
- Códigos en documentos impresos

**Consejo**: Para mejores resultados, mantén el código centrado en el recuadro verde y espera 1-2 segundos sin mover la cámara.
