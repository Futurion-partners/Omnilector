import hashlib
import json

import cv2
import httpx

addr = 'http://localhost:8000/'
test_url = addr + 'detect-barcode'

# prepare headers for http request
# content_type = 'image/jpeg'
headers = {
    # 'content-type': content_type,
}

img = cv2.imread('20250906_113822.jpg')
img = cv2.imread('image.png')
if img is None:
    raise ValueError("Image not found or unable to load.")

# encode image as jpeg
_, img_encoded = cv2.imencode(
    '.jpg',
    img,
    []
)

if img_encoded is None:
    raise ValueError('Image could not be encoded')


# send http request with image and receive response
contents = img_encoded.tobytes()
print('hash:', hashlib.sha256(contents).hexdigest())

response = httpx.post(
    test_url,
    files={
        "file": contents
    },
    headers=headers,
)
# decode response
print(json.loads(response.text))
