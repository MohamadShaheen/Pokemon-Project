from fastapi import APIRouter, HTTPException

from routers.pokemons_router import add_new_pokemon
from routers.trainers_router import add_pokemon_to_trainer
from utils.api_operations import get_pokemon_details, get_evolved_pokemon
from database_connection.database import session_local
from database_connection.models import Pokemon, Type, TypePokemon, Trainer, TrainerPokemon

router = APIRouter()


@router.put('/')
async def evolve_pokemon_of_trainer(pokemon_name: str, trainer_name: str):
    session = session_local()
    db_pokemon = session.query(Pokemon).filter(Pokemon.name == pokemon_name).first()

    if db_pokemon is None:
        session.close()
        raise HTTPException(status_code=404, detail='Pokemon not found')

    db_trainer = session.query(Trainer).filter(Trainer.name == trainer_name).first()

    if db_trainer is None:
        session.close()
        raise HTTPException(status_code=404, detail='Trainer not found')

    db_trainer_pokemon = session.query(TrainerPokemon).filter(TrainerPokemon.trainer_id == db_trainer.id,
                                                              TrainerPokemon.pokemon_id == db_pokemon.id).first()

    if db_trainer_pokemon is None:
        session.close()
        raise HTTPException(status_code=404, detail='Trainer does not have this Pokemon')

    evolved_pokemon = get_evolved_pokemon(pokemon_name=pokemon_name)
    if evolved_pokemon is None:
        return f'Pokemon can not be evolved anymore'

    session.delete(db_trainer_pokemon)
    session.commit()
    session.close()

    try:
        await add_new_pokemon(pokemon_name=evolved_pokemon)
    except HTTPException:
        pass

    try:
        await add_pokemon_to_trainer(pokemon_name=evolved_pokemon, trainer_name=trainer_name)
    except HTTPException:
        pass

    return f'Pokemon {pokemon_name} has been evolved to {evolved_pokemon} for trainer {trainer_name}'
