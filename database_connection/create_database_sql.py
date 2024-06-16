import json
import os

from dotenv import load_dotenv
from sqlalchemy import text

from database_connection.database import session_local, Base, engine, temp_engine
from database_connection.models import Pokemon, Trainer, Type, TrainerPokemon, TypePokemon

session = session_local()

load_dotenv()

database_name = os.getenv('SQL_DATABASE_NAME')


def create_database():
    with temp_engine.connect() as connection:
        result = connection.execute(text(f'SHOW DATABASES LIKE \'{database_name}\''))
        database_exists = result.scalar()

        if database_exists is None:
            connection.execute(text(f'CREATE DATABASE {database_name}'))
            print(f'Database {database_name} created successfully!')
        else:
            print(f'Database {database_name} already exists!')

    Base.metadata.create_all(engine)

    with open('data/pokemons_data.json', 'r') as file:
        data = json.load(file)

    for entry in data:
        db_pokemon = session.query(Pokemon).filter(Pokemon.name == entry['name']).first()
        if not db_pokemon:
            db_pokemon = Pokemon(id=entry['id'], name=entry['name'], height=entry['height'], weight=entry['weight'])
            session.add(db_pokemon)
            session.flush()

        for trainer in entry['ownedBy']:
            db_trainer = session.query(Trainer).filter(Trainer.name == trainer['name']).first()
            if not db_trainer:
                db_trainer = Trainer(name=trainer['name'], town=trainer['town'])
                session.add(db_trainer)
                session.flush()

            db_trainer_pokemon = TrainerPokemon(trainer_id=db_trainer.id, pokemon_id=db_pokemon.id)
            session.add(db_trainer_pokemon)
            session.flush()

        for type in entry['types']:
            db_type = session.query(Type).filter(Type.type == type).first()
            if not db_type:
                db_type = Type(type=type)
                session.add(db_type)
                session.flush()

            db_type_pokemon = TypePokemon(type_id=db_type.id, pokemon_id=db_pokemon.id)
            session.add(db_type_pokemon)
            session.flush()

    session.commit()
    session.close()