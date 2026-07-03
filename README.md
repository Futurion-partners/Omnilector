# 📷 Futurion Barcode - API de Detección de Códigos de Barras

Procesa varios tipos de códigos de barras y QR con facilidad. La API ofrece procesamiento de imágenes estáticas mediante REST y detección en tiempo real a través de WebSockets.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.13+-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116+-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

## ✨ Características Principales

- 🔍 **Multi-motor de detección**: PyZbar, ZXing-C++ y OpenCV WeChat QR
- 📡 **WebSocket streaming**: Detección en tiempo real con baja latencia
- 🖼️ **API REST**: Procesamiento de imágenes estáticas
- 🎯 **ROI dinámico**: Enfoque en región de interés para mayor precisión
- ✅ **Sistema de confianza**: Confirmación de códigos detectados
- 🐳 **Docker ready**: Listo para contenedores
- 📚 **Documentación completa**: Swagger UI integrado

## 📋 Formatos Soportados

### Códigos de Barras 1D
EAN-8, EAN-13, UPC-A, UPC-E, Code 39, Code 93, Code 128, ITF, Codabar

### Códigos 2D
QR Code, Aztec Code, DataMatrix, PDF417

---

## 🚀 Inicio Rápido

```bash
# 1. Instalar uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clonar proyecto
git clone https://github.com/Futurion-partners/barcode-2.git
cd barcode-2

# 3. Instalar dependencias
uv sync

# 4. Ejecutar servidor
uv run futurion-barcode-dev

# 5. Abrir navegador
# http://localhost:8000
```

Ver **[QUICKSTART.md](QUICKSTART.md)** para instrucciones detalladas.

---

## 📚 Documentación Completa

| Documento | Descripción |
|-----------|-------------|
| **[QUICKSTART.md](QUICKSTART.md)** | ⏱️ Guía de inicio en 5 minutos |
| **[DOCUMENTATION.md](DOCUMENTATION.md)** | 📖 Documentación técnica completa |
| **[API_REFERENCE.md](API_REFERENCE.md)** | 📡 Referencia de la API REST y WebSocket |
| **[FRONTEND_GUIDE.md](FRONTEND_GUIDE.md)** | 🎨 Guía del cliente web JavaScript |

---

## 📋 Tabla de Contenidos

- [Futurion Barcode](#futurion-barcode)
  - [Inicio Rápido](#inicio-rápido)
  - [Documentación Completa](#documentación-completa)
  - [Tabla de Contenidos](#tabla-de-contenidos)
  - [Ejecutar y Configurar el Proyecto](#ejecutar-y-configurar-el-proyecto)
    - [Con Docker](#con-docker)
      - [Ejecutar la Imagen Docker](#ejecutar-la-imagen-docker)
        - [Construir la Imagen Docker](#construir-la-imagen-docker)
        - [Ejecutar la API](#ejecutar-la-api)
          - [Modificar Puertos](#modificar-puertos)
    - [Desarrollo Local](#desarrollo-local)
      - [Configuración Local](#configuración-local)
      - [Ejecutar Localmente](#ejecutar-localmente)
        - [Recarga Activada](#recarga-activada)
        - [Recarga Desactivada](#recarga-desactivada)

---

## 🎯 Uso Básico

### Interfaz Web (Recomendado)

1. Inicia el servidor: `uv run futurion-barcode-dev`
2. Abre http://localhost:8000 en tu navegador
3. Haz clic en "📷 Iniciar Cámara"
4. Haz clic en "🔌 Conectar WebSocket"
5. Apunta tu cámara al código de barras

### API REST

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

Ver **[API_REFERENCE.md](API_REFERENCE.md)** para más ejemplos.

---

## 🛠️ Ejecutar y Configurar el Proyecto

### Con Docker

Es posible que desees regenerar el archivo `.dockerignore` si modificaste
los archivos `.gitignore` o `.prodignore`. Puedes hacerlo ejecutando
los siguientes comandos:

> [!NOTE]
> Este comando sobrescribirá el archivo `.dockerignore` con todo el
> contenido de los archivos `.gitignore` y `.prodignore`.

```sh
cat .gitignore .prodignore > .dockerignore
```

#### Ejecutar la Imagen Docker

##### Construir la Imagen Docker

```sh
docker build -t futurion-barcode:$(git rev-parse --short HEAD) . # Etiquetar con el hash del commit actual
docker build -t futurion-barcode:latest . # Etiquetar como latest
```

##### Ejecutar la API

Una vez que hayas [construido](#construir-la-imagen-docker) la imagen, puedes ejecutar
el siguiente comando:

```sh
docker run --rm -p 8000:8000 futurion-barcode:latest
```

Ahora puedes ir a la [documentación generada](http://127.0.0.1:8000/docs)
y revisar la API.

###### Modificar Puertos

Puedes configurar un puerto estableciendo una variable de entorno `PORT` al
número de puerto deseado.

Por defecto está configurado en `8000`. En caso de que quieras cambiar el
número de puerto interno, puedes hacerlo ejecutando el siguiente comando,
que establecerá el número de puerto en `8080` y luego mapeará el puerto `80` de
la máquina host al puerto `8080` del contenedor.

```bash
docker run --rm -e PORT=8080 -p 80:8080 futurion-barcode:latest
```

Y la API debería ser accesible en
[http://127.0.0.1:80/](http://127.0.0.1:80/docs)

##### Usar docker-compose

Alternativamente, puedes usar docker-compose para construir y ejecutar:

```bash
docker compose up --build
```

Esto expone el servicio en http://localhost:8000 e incluye un healthcheck.

---

## 📡 Endpoints

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Redirige a `/test` |
| `/test` | GET | Cliente web completo |
| `/docs` | GET | Documentación interactiva (Swagger) |
| `/health` | GET | Health check |
| `/api/v1/image/` | POST | Procesar imagen estática |
| `/api/v1/realtime/` | WebSocket | Detección en tiempo real |

---

## 🐳 Despliegue en Dokploy

Para desplegar en [Dokploy](https://dokploy.com/), un PaaS auto-hospedado:

1. **Construir y Desplegar**: Sube tu código a tu repositorio Git. Dokploy construirá usando el Dockerfile o pyproject.toml.

2. **Dependencias**: Asegúrate de que todas las dependencias estén listadas en `pyproject.toml`. Si encuentras `ModuleNotFoundError`, revisa los logs de construcción y redespliega después de agregar los paquetes faltantes (ej: `pillow` fue agregado para procesamiento de imágenes).

3. **Variables de Entorno**:
   - Establece `BARCODE_ONLY_PYZBAR=1` para priorizar PyZbar (por defecto).
   - Ajusta `PORT` si es necesario (por defecto 8000).

4. **Solución de Problemas**:
   - **Módulos Faltantes**: Si la construcción falla con errores de importación, agrega el paquete faltante a las dependencias de `pyproject.toml` y redespliega.
   - **Verificación de Versión**: Después del despliegue, visita `/api/v1/version` para confirmar la versión y que la app se inició correctamente.
    - **Logs**: Revisa los logs de Dokploy para errores como "No module named 'PIL'" – indica que Pillow no está instalado; agrega `pillow>=12.0.0` a las dependencias.
   - **Redesplegar**: Fuerza una reconstrucción enviando un nuevo commit o activando una reconstrucción manual en Dokploy.
   - **Health**: La app incluye un endpoint de healthcheck en `/health` (si está configurado en el Dockerfile).

### Desarrollo Local

> [!TIP]
> Si no estás familiarizado con [uv](https://docs.astral.sh/uv/),
> puedes revisar [este video](https://youtu.be/AMdG7IjgSPM)

#### Configuración Local

1. Instala
[uv](https://docs.astral.sh/uv/getting-started/installation/) si no está
presente en tu máquina

1. Instala/Sincroniza los paquetes requeridos

    ```sh
    uv sync
    ```

¡Y eso es todo!

#### Ejecutar Localmente

Para ejecutar los siguientes comandos, primero debes
[configurar este proyecto localmente](#configuración-local). Más importante aún,
debes tener tus paquetes sincronizados.

Una vez que hayas hecho eso, puedes:

Ejecutar con recarga [activada](#recarga-activada) o
[desactivada](#recarga-desactivada)

##### Recarga Activada

Esto actualizará la instancia de la API una vez que un archivo haya sido actualizado

```sh
uv run futurion-barcode-dev
```

##### Recarga Desactivada

Esto ejecutará la API con el estado actual del proyecto y **no**
se actualizará cuando modifiques tu código.

```sh
uv run futurion-barcode
```

---

## 🧪 Testing

```bash
# Ejecutar tests
pytest

# Con cobertura
pytest --cov=src/futurion_barcode

# Tests de integración
pytest tests/integration/
```

---

## 🤝 Contribuir

1. Fork el repositorio
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit tus cambios: `git commit -m "feat: agregar nueva funcionalidad"`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

Ver **[DOCUMENTATION.md](DOCUMENTATION.md)** sección "Desarrollo y Contribución" para más detalles.

---

## 📊 Rendimiento

- **Latencia API REST**: ~50-80 ms por imagen
- **Latencia WebSocket**: ~100-150 ms total
- **Throughput**: ~10-15 detecciones/segundo por conexión
- **Tasa de detección**: 95-98% para códigos comunes

---

## 🔧 Variables de Entorno

```env
PORT=8000                    # Puerto del servidor
HOST=0.0.0.0                 # Host del servidor
LOG_LEVEL=info               # Nivel de logging
BARCODE_ONLY_PYZBAR=0        # Solo usar PyZbar (1=sí, 0=no)
```

---

## 🆘 Solución de Problemas

### No se detectan códigos
- ✅ Verifica que el código esté dentro del recuadro verde
- ✅ Mejora la iluminación
- ✅ Aumenta la calidad JPEG a 0.90-0.95
- ✅ Activa "Modo PNG sin pérdida"

### Cámara no funciona
- ✅ Permite permisos de cámara en el navegador
- ✅ Usa HTTPS en producción
- ✅ Prueba con otro navegador (Chrome recomendado)

Ver **[DOCUMENTATION.md](DOCUMENTATION.md)** sección "Solución de Problemas" para más casos.

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

---

## 👥 Autores

- **Harrison Pinto** - [@Futurion-partners](https://github.com/Futurion-partners)

---

## 📞 Soporte

- **GitHub Issues**: [github.com/Futurion-partners/barcode-2/issues](https://github.com/Futurion-partners/barcode-2/issues)
- **Email**: support@futurion.com



