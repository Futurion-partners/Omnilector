# Guía de Contribución - Omnilector

¡Gracias por tu interés en contribuir a **Omnilector**! Como proyecto de código abierto, valoramos cualquier tipo de contribución, ya sea reportando errores, sugiriendo mejoras, escribiendo documentación o enviando Pull Requests con código nuevo.

---

## 📋 Código de Conducta

Al participar en este proyecto, te comprometes a seguir nuestro [Código de Conducta](CODE_OF_CONDUCT.md). Por favor, trátanos a todos con respeto y profesionalismo.

---

## 🛠️ Cómo Empezar

### 1. Requisitos Previos
Asegúrate de tener instalado:
* **Python 3.13** o superior.
* **uv** (el gestor de paquetes y entornos de Python recomendado). Puedes instalarlo con:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
  *(En Windows puedes usar `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`).*

### 2. Clonar el Repositorio
Haz un fork del repositorio en GitHub y luego clónalo localmente:
```bash
git clone https://github.com/tu-usuario/Omnilector.git
cd Omnilector
```

### 3. Configurar el Entorno de Desarrollo
Instala todas las dependencias (incluyendo las de desarrollo) y sincroniza el entorno:
```bash
uv sync
```

### 4. Ejecutar el Servidor localmente
Para iniciar el servidor de desarrollo con recarga automática:
```bash
uv run omnilector-dev
```
El servidor estará disponible en `http://localhost:8000`.

---

## 💡 Cómo Contribuir Cambios

### Reportar Errores o Sugerir Características
Si encuentras un error o tienes una idea para mejorar, busca primero en la sección de **Issues** para ver si ya se está discutiendo. Si no es así, abre una nueva Issue usando nuestras plantillas correspondientes.

### Enviar un Pull Request (PR)
1. Crea una rama descriptiva para tus cambios:
   ```bash
   git checkout -b feature/mi-nueva-caracteristica
   ```
2. Realiza tus cambios en el código asegurándote de seguir el estilo del proyecto.
3. Formatea tu código y realiza chequeos de linter si tienes las herramientas instaladas.
4. Haz commit de tus cambios con mensajes claros:
   ```bash
   git commit -m "feat: agregar soporte para nuevo formato de código de barras"
   ```
5. Sube tu rama a tu fork:
   ```bash
   git push origin feature/mi-nueva-caracteristica
   ```
6. Abre un Pull Request contra la rama `main` del repositorio oficial de **Omnilector**. Asegúrate de rellenar la plantilla de PR con toda la información solicitada.

¡Gracias de nuevo por tu ayuda para mejorar Omnilector!
