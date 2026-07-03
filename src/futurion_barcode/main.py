from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

from futurion_barcode.routes import api_router
from importlib.metadata import version


app = FastAPI(
    title="Barcode Detection API",
    version=version("futurion_barcode")
)

# CORS (in case you use it from the browser)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api_router)


# Root: redirect to /test for convenience when opening base URL
@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url="/test", status_code=307)

# Health check endpoint for uptime checks
@app.get("/health", response_class=JSONResponse, include_in_schema=False)
def health():
    return {"status": "ok"}


# Simple test page served by FastAPI (to allow HTTPS via a single origin)
@app.get("/test", response_class=HTMLResponse)
def websocket_test_page() -> str:
    # Project root is two levels up from this file (src/futurion_barcode/main.py)
    root = Path(__file__).resolve().parents[2]
    html_path = root / "websocket_test.html"
    
    print(f"Looking for HTML file at: {html_path}")
    print(f"File exists: {html_path.exists()}")
    
    try:
        content = html_path.read_text(encoding="utf-8")
        print(f"Successfully read {len(content)} characters")
        return content
    except FileNotFoundError:
        error_msg = f"<h1>websocket_test.html no encontrado</h1><p>Buscando en: {html_path}</p><p>Archivo existe: {html_path.exists()}</p>"
        print(f"Error: File not found at {html_path}")
        return error_msg
    except Exception as e:
        error_msg = f"<h1>Error al leer archivo</h1><p>Error: {e}</p><p>Ruta: {html_path}</p>"
        print(f"Error reading file: {e}")
        return error_msg


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
