import uvicorn

from futurion_barcode.main import app
from os import getenv

PORT = int(getenv("PORT", 8000))
HOST = "0.0.0.0"


def main() -> None:
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
    )


def reload() -> None:
    uvicorn.run(
        "futurion_barcode.main:app",
        host=HOST,
        port=PORT,
        reload=True,
    )
