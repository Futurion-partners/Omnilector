from pydantic import BaseModel


class BarcodeResponse(BaseModel):
    barcodes: list[str]
    locations: list[list[list[float]]]
    # Fuente del detector para cada código (p. ej., 'pyzbar' o 'zxing')
    sources: list[str] = []
