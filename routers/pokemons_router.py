from fastapi import APIRouter, HTTPException
from utils.api_operations import get_pokemon_details
from database_connection.database import session_local
from database_connection.models import Pokemon, Trainer, Type, TypePokemon, TrainerPokemon

router = APIRouter()


@router.get('/')
async def get_pokemon_details_by_id(pokemon_id: int):
    session = session_local()
    db_pokemon = session.query(Pokemon).filter(Pokemon.id == pokemon_id).first()

    if db_pokemon is None:
        session.close()
        raise HTTPException(status_code=404, detail='Pokemon not found')

    session.close()

    return db_pokemon


@router.get('/by-name/')
async def get_pokemon_details_by_name(pokemon_name: str):
    session = session_local()
    db_pokemon = session.query(Pokemon).filter(Pokemon.name == pokemon_name).first()

    if db_pokemon is None:
        session.close()
        raise HTTPException(status_code=404, detail='Pokemon not found')

    session.close()

    return db_pokemon


@router.get('/by-type/')
async def get_pokemons_by_type(pokemon_type: str):
    session = session_local()
    db_type = session.query(Type).filter(Type.type == pokemon_type).first()

    if db_type is None:
        session.close()
        raise HTTPException(status_code=404, detail='Type not found')

    db_pokemons = session.query(TypePokemon).filter(TypePokemon.type_id == db_type.id).all()
    pokemons = []
    for item in db_pokemons:
        db_pokemon = session.query(Pokemon).filter(Pokemon.id == item.pokemon.id).first()
        pokemons.append(db_pokemon.name)

    session.close()

    return pokemons


@router.get('/by-trainer/')
async def get_pokemons_by_trainer(trainer_name: str):
    session = session_local()
    db_trainer = session.query(Trainer).filter(Trainer.name == trainer_name).first()

    if db_trainer is None:
        session.close()
        raise HTTPException(status_code=404, detail='Trainer not found')

    db_pokemons = session.query(TrainerPokemon).filter(TrainerPokemon.trainer_id == db_trainer.id).all()
    pokemons = []
    for item in db_pokemons:
        db_pokemon = session.query(Pokemon).filter(Pokemon.id == item.pokemon.id).first()
        pokemons.append(db_pokemon.name)

    session.close()

    return pokemons


@router.post('/')
async def add_new_pokemon(pokemon_name: str):
    session = session_local()
    db_pokemon = session.query(Pokemon).filter(Pokemon.name == pokemon_name).first()

    if db_pokemon:
        session.close()
        raise HTTPException(status_code=409, detail='Pokemon already exists')

    types, height, weight = get_pokemon_details(pokemon_name=pokemon_name)

    if types is None or height is None or weight is None:
        session.close()
        raise HTTPException(status_code=400, detail='Failed to get pokemon details. No pokemon with the provided name exists')

    db_pokemon = Pokemon(name=pokemon_name, height=height, weight=weight)
    session.add(db_pokemon)
    session.flush()

    for type in types:
        db_type = session.query(Type).filter(Type.type == type).first()
        if db_type is None:
            db_type = Type(type=type)
            session.add(db_type)
            session.flush()

        db_type_pokemon = TypePokemon(type_id=db_type.id, pokemon_id=db_pokemon.id)
        session.add(db_type_pokemon)
        session.flush()

    session.commit()
    session.close()

    return {'name': pokemon_name, 'height': height, 'weight': weight, 'types': types}


@router.delete('/')
async def delete_pokemon_by_name(pokemon_name: str):
    session = session_local()
    db_pokemon = session.query(Pokemon).filter(Pokemon.name == pokemon_name).first()

    if db_pokemon is None:
        session.close()
        raise HTTPException(status_code=404, detail='Pokemon not found')

    db_types = session.query(TypePokemon).filter(TypePokemon.pokemon_id == db_pokemon.id).all()
    for db_type in db_types:
        session.delete(db_type)

    db_trainers = session.query(TrainerPokemon).filter(TrainerPokemon.pokemon_id == db_pokemon.id).all()
    for db_trainer in db_trainers:
        session.delete(db_trainer)

    session.delete(db_pokemon)
    session.commit()
    session.close()

    return f'Pokemon {pokemon_name} was deleted successfully'
