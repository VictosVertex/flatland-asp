
import base64
import io
from typing import Any

from PIL import Image


def get_image_bytes_from_image(image: Image.Image) -> str:
    byte_stream = io.BytesIO()
    image.save(byte_stream, format='PNG')
    image_bytes = byte_stream.getvalue()
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    return image_base64
