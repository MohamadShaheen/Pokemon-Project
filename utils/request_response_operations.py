import base64
import requests
from PIL import Image
from io import BytesIO
from urllib.parse import urlparse


def get_image_by_url(image_url):
    parsed_url = urlparse(image_url)

    if not parsed_url.scheme:
        return None

    response = requests.get(image_url)

    if response.status_code == 200:
        try:
            image = Image.open(BytesIO(response.content))

            image_byte_array = BytesIO()
            image.save(image_byte_array, format='PNG')
            image_byte_array = image_byte_array.getvalue()

            return image_byte_array

        except Exception:
            return None
    else:
        return None


def get_base64_image_by_url(image_url):
    response = requests.get(image_url)
    image_byte_array = base64.b64encode(response.content).decode('utf-8')

    return image_byte_array
