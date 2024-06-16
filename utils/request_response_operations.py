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

            image_byte_arr = BytesIO()
            image.save(image_byte_arr, format='PNG')
            image_byte_arr = image_byte_arr.getvalue()

            return image_byte_arr

        except Exception:
            return None
    else:
        return None
