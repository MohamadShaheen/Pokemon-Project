from fastapi import APIRouter, HTTPException
from DAL.poke_data_interactor import PokeDbInteractor

router = APIRouter()


@router.get('/')
async def get_pokemon_details_by_id(pokemon_id: int):
    try:
        pok = PokeDbInteractor()
        res = pok.get_poke_details_by_id(pokemon_id)
        return res
    except HTTPException as e:
        raise e


@router.get('/by-name/')
async def get_pokemon_details_by_name(pokemon_name: str):
    pok = PokeDbInteractor()
    res = pok.get_pokemon_details_by_name(pokemon_name)
    return res


@router.get('/by-type/')
async def get_pokemons_by_type(pokemon_type: str):
    pok = PokeDbInteractor()
    res = pok.get_pokemons_by_type(pokemon_type)
    return res



@router.get('/by-trainer/')
async def get_pokemons_by_trainer(trainer_name: str):
    pok = PokeDbInteractor()
    res = pok.get_pokemons_by_trainer(trainer_name)
    return res


@router.post('/')
async def add_new_pokemon(pokemon_name: str):
    pok = PokeDbInteractor()
    res = pok.add_new_pokemon(pokemon_name)
    return res

@router.delete('/')
async def delete_pokemon_by_name(pokemon_name: str):
    pok = PokeDbInteractor()
    res = pok.delete_pokemon_by_name(pokemon_name)
    return res

