from fastapi import APIRouter, HTTPException
from DAL.trainers_interactor import TrainersInteractor

router = APIRouter()


@router.put('/')
async def delete_pokemon_of_trainer(pokemon_name, trainer_name):
    trainers_interactor = TrainersInteractor()
    response = trainers_interactor.delete_pokemon_of_trainer(pokemon_name=pokemon_name, trainer_name=trainer_name)

    if response == 1:
        raise HTTPException(status_code=404, detail='Pokemon not found')

    if response == 2:
        raise HTTPException(status_code=404, detail='Trainer not found')

    if response == 3:
        raise HTTPException(status_code=404, detail='Trainer does not own this pokemon')

    return response


@router.get('/')
async def get_pokemon_trainers(pokemon_name: str):
    trainers_interactor = TrainersInteractor()
    trainers = trainers_interactor.get_pokemon_trainers(pokemon_name=pokemon_name)

    if trainers is None:
        raise HTTPException(status_code=404, detail='Pokemon not found')

    return trainers


@router.post('/pokemon/')
async def add_pokemon_to_trainer(pokemon_name: str, trainer_name: str):
    trainers_interactor = TrainersInteractor()
    response = trainers_interactor.add_pokemon_to_trainer(pokemon_name=pokemon_name, trainer_name=trainer_name)

    if response == 1:
        raise HTTPException(status_code=404, detail='Pokemon not found')

    if response == 2:
        raise HTTPException(status_code=404, detail='Trainer not found')

    if response == 3:
        raise HTTPException(status_code=409, detail='Trainer already owns this Pokemon')

    return response


@router.post('/trainer/')
async def create_trainer(trainer_name: str, trainer_town: str):
    trainers_interactor = TrainersInteractor()
    response = trainers_interactor.create_trainer(trainer_name=trainer_name, trainer_town=trainer_town)

    if response is None:
        raise HTTPException(status_code=409, detail='Trainer already exists')

    return response


@router.delete('/')
async def delete_trainer_by_name(trainer_name: str):
    trainers_interactor = TrainersInteractor()
    response = trainers_interactor.delete_trainer_by_name(trainer_name=trainer_name)

    if response is None:
        raise HTTPException(status_code=404, detail='Trainer not found')

    return response
