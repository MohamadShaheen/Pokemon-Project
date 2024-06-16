from fastapi import APIRouter, HTTPException
from DAL.evolve_interactor import EvolveInteractor

router = APIRouter()


@router.put('/')
async def evolve_pokemon_of_trainer(pokemon_name: str, trainer_name: str):
    evolve_interactor = EvolveInteractor()
    response = evolve_interactor.evolve_pokemon_of_trainer(pokemon_name=pokemon_name, trainer_name=trainer_name)

    if response == 1:
        raise HTTPException(status_code=404, detail='Pokemon not found')

    if response == 2:
        raise HTTPException(status_code=404, detail='Trainer not found')

    if response == 3:
        raise HTTPException(status_code=404, detail='Trainer does not have this Pokemon')

    if response == 4:
        raise HTTPException(status_code=400, detail='Pokemon cannot be evolved anymore')

    return response
