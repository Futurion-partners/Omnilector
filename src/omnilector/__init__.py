import uvicorn

from omnilector.main import app
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
        "omnilector.main:app",
        host=HOST,
        port=PORT,
        reload=True,
    )
