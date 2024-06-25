import json

from fastapi import APIRouter, HTTPException

from DAL.trainer_battle_interactor import TrainerBattle
from DAL.pokemons_interactor import PokemonsInteractor

router = APIRouter()


@router.put('/')
async def Battle(trainer1_name, trainer2_name):
    pokemons_interactor = PokemonsInteractor()
    trainer1_pokemons = pokemons_interactor.get_pokemons_by_trainer(trainer1_name)

    trainer2_pokemons = pokemons_interactor.get_pokemons_by_trainer(trainer2_name)

    battle = TrainerBattle(trainer1_name, trainer2_name, trainer1_pokemons, trainer2_pokemons)
    #print(json.dumps(battle.simulate_battle(), indent=4))
    return battle.simulate_battle()
