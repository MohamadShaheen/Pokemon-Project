from fastapi import APIRouter, HTTPException
from database_connection.database import session_local
from database_connection.models import Pokemon, Trainer, TrainerPokemon
from DAL.trainer_data_interactor import TrainerDbInteractor
router = APIRouter()


@router.put('/')
async def delete_pokemon_of_trainer(pokemon_name, trainer_name):
    trainers = TrainerDbInteractor()
    res = trainers.delete_pokemon_of_trainer(pokemon_name, trainer_name)
    return res

@router.get('/')
async def get_pokemon_trainers(pokemon_name: str):
    trainers = TrainerDbInteractor()
    res = trainers.get_pokemon_trainers(pokemon_name)
    return res


@router.post('/pokemon/')
async def add_pokemon_to_trainer(pokemon_name: str, trainer_name: str):
    trainers = TrainerDbInteractor()
    res = trainers.add_pokemon_to_trainer(pokemon_name, trainer_name)
    return res

@router.post('/trainer/')
async def create_trainer(trainer_name: str, trainer_town: str):
    trainers = TrainerDbInteractor()
    res = trainers.create_trainer(trainer_name, trainer_town)
    return res

@router.delete('/')
async def delete_trainer_by_name(trainer_name: str):
    trainers = TrainerDbInteractor()
    res = trainers.delete_trainer_by_name(trainer_name)
    return res