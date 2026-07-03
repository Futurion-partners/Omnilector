from hashlib import sha256

from fastapi import APIRouter, File, UploadFile

from futurion_barcode.models.responses.barcode import BarcodeResponse
from futurion_barcode.utils.image import process_image

router = APIRouter(
    prefix='/image',
    tags=[
        'image',
    ]
)


@router.post(
    "/",
    response_model=BarcodeResponse
)
async def detect_barcode(file: UploadFile = File(...)):
    contents = await file.read()
    print("File hash:", sha256(contents).hexdigest())
    return await process_image(contents)
