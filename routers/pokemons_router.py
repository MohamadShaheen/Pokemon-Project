from fastapi import APIRouter, HTTPException
from DAL.images_interactor import ImagesInteractor
from DAL.pokemons_interactor import PokemonsInteractor

router = APIRouter()


@router.get('/')
async def get_pokemon_details_by_id(pokemon_id: int):
    pokemon_interactor = PokemonsInteractor()
    pokemon = pokemon_interactor.get_pokemon_details_by_id(pokemon_id=pokemon_id)

    if pokemon is None:
        raise HTTPException(status_code=404, detail='Pokemon not found')

    images_interactor = ImagesInteractor()
    images_interactor.show_image_by_id(pokemon_id=pokemon_id)

    return pokemon


@router.get('/by-name/')
async def get_pokemon_details_by_name(pokemon_name: str):
    pokemon_interactor = PokemonsInteractor()
    pokemon = pokemon_interactor.get_pokemon_details_by_name(pokemon_name=pokemon_name)

    if pokemon is None:
        raise HTTPException(status_code=404, detail='Pokemon not found')

    images_interactor = ImagesInteractor()
    images_interactor.show_image_by_name(pokemon_name=pokemon_name)

    return pokemon


@router.get('/by-type/')
async def get_pokemons_by_type(pokemon_type: str):
    pokemon_interactor = PokemonsInteractor()
    pokemons = pokemon_interactor.get_pokemons_by_type(pokemon_type=pokemon_type)

    if pokemons is None:
        raise HTTPException(status_code=404, detail='Type not found')

    return pokemons


@router.get('/by-trainer/')
async def get_pokemons_by_trainer(trainer_name: str):
    pokemon_interactor = PokemonsInteractor()
    pokemons = pokemon_interactor.get_pokemons_by_trainer(trainer_name=trainer_name)

    if pokemons is None:
        raise HTTPException(status_code=404, detail='Trainer not found')

    return pokemons


@router.post('/')
async def add_new_pokemon(pokemon_name: str):
    pokemon_interactor = PokemonsInteractor()
    response = pokemon_interactor.add_new_pokemon(pokemon_name=pokemon_name)

    if response == 1:
        raise HTTPException(status_code=409, detail='Pokemon already exists')

    if response == 2:
        raise HTTPException(status_code=400, detail='Failed to get pokemon details. No pokemon with the provided name exists')

    images_interactor = ImagesInteractor()
    images_interactor.insert_image(pokemon_name=pokemon_name)
    images_interactor.show_image_by_name(pokemon_name=pokemon_name)

    return response


@router.delete('/')
async def delete_pokemon_by_name(pokemon_name: str):
    pokemon_interactor = PokemonsInteractor()
    response = pokemon_interactor.delete_pokemon_by_name(pokemon_name=pokemon_name)

    if response is None:
        raise HTTPException(status_code=404, detail='Pokemon not found')

    images_interactor = ImagesInteractor()
    images_interactor.show_image_by_name(pokemon_name=pokemon_name)
    images_interactor.delete_image(pokemon_name=pokemon_name)

    return f'Pokemon {pokemon_name} was deleted successfully'
