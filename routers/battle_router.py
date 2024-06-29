import json
from fastapi import APIRouter, HTTPException
from DAL.battle_interactor import BattleInteractor

router = APIRouter()


@router.get('/')
async def simulate_battle(trainer1_name: str, pokemon1_name: str, trainer2_name: str, pokemon2_name: str):
    battle_interactor = BattleInteractor()
    response = battle_interactor.simulate_battle(trainer1_name, pokemon1_name, trainer2_name, pokemon2_name)

    if response == 1:
        raise HTTPException(status_code=404, detail=f'Trainer {trainer1_name} does not exist')

    elif response == 2:
        raise HTTPException(status_code=404, detail=f'Trainer {trainer2_name} does not exist')

    elif response == 3:
        raise HTTPException(status_code=404, detail=f'{trainer1_name} does not have {pokemon1_name} in his collection')

    elif response == 4:
        raise HTTPException(status_code=404, detail=f'{trainer2_name} does not have {pokemon2_name} in his collection')

    elif response == 5:
        raise HTTPException(status_code=409, detail=f'{trainer2_name} already has {pokemon1_name} in his collection')

    elif response == 6:
        raise HTTPException(status_code=409, detail=f'{trainer1_name} already has {pokemon2_name} in his collection')

    return response


@router.get('/detailed-logs/')
async def get_detailed_battle_logs():
    with open('data/detailed_battle_logs.json', 'r') as file:
        detailed_battle_logs = json.load(file)

    return detailed_battle_logs


@router.get('/brief-logs/')
async def get_detailed_battle_logs():
    with open('data/brief_battle_logs.json', 'r') as file:
        brief_battle_logs = json.load(file)

    return brief_battle_logs
