from io import BytesIO

from PIL import Image
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from DAL.images_interactor import ImagesInteractor

router = APIRouter()


@router.get('/')
async def show_pokemon_image_by_id(pokemon_id: int):
    images_interactor = ImagesInteractor()
    response = images_interactor.get_image_by_id(pokemon_id=pokemon_id)

    if response is None:
        raise HTTPException(status_code=404, detail='Pokemon with the given name not found')

    image_byte_arr = response['pokemon_image']
    image = Image.open(BytesIO(image_byte_arr))

    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return StreamingResponse(img_byte_arr, media_type="image/png")


@router.get('/by-name')
async def show_pokemon_image_by_name(pokemon_name: str):
    images_interactor = ImagesInteractor()
    response = images_interactor.get_image_by_name(pokemon_name=pokemon_name)

    if response is None:
        raise HTTPException(status_code=404, detail='Pokemon with the given name not found')

    image_byte_arr = response['pokemon_image']
    image = Image.open(BytesIO(image_byte_arr))

    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return StreamingResponse(img_byte_arr, media_type="image/png")
