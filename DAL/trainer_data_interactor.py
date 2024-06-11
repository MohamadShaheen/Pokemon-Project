from database_connection.database import session_local
from database_connection.models import Pokemon, Trainer, Type, TypePokemon, TrainerPokemon
from fastapi import HTTPException
from utils.api_operations import get_pokemon_details

class TrainerDbInteractor:
    def __init__(self):
        self.session = session_local()

    def delete_pokemon_of_trainer(self, pokemon_name, trainer_name):
        with self.session as session:
            db_pokemon = session.query(Pokemon).filter(Pokemon.name == pokemon_name).first()
            if not db_pokemon:
                raise HTTPException(status_code=404, detail='Pokemon not found')
            db_trainer = session.query(Trainer).filter(Trainer.name == trainer_name).first()
            if not db_trainer:
                raise HTTPException(status_code=404, detail='Trainer not found')
            trainer_pokemon = session.query(TrainerPokemon).filter(TrainerPokemon.trainer_id == db_trainer.id,
                                                                   TrainerPokemon.pokemon_id == db_pokemon.id).first()
            if not trainer_pokemon:
                raise HTTPException(status_code=404, detail='Trainer does not own this pokemon')
            session.delete(trainer_pokemon)
            session.commit()
            return f'Pokemon {pokemon_name} was successfully deleted from trainer {trainer_name}'

    def get_pokemon_trainers(self, pokemon_name: str):
        with self.session as session:
            db_pokemon = session.query(Pokemon).filter(Pokemon.name == pokemon_name).first()
            if db_pokemon is None:
                raise HTTPException(status_code=404, detail='Pokemon not found')
            db_trainers = session.query(TrainerPokemon).filter(TrainerPokemon.pokemon_id == db_pokemon.id).all()
            trainers = []
            for item in db_trainers:
                db_trainer = session.query(Trainer).filter(Trainer.id == item.trainer.id).first()
                trainers.append(db_trainer.name)
            return trainers

    def add_pokemon_to_trainer(self, pokemon_name: str, trainer_name: str):
        with self.session as session:
            db_pokemon = session.query(Pokemon).filter(Pokemon.name == pokemon_name).first()
            if db_pokemon is None:
                raise HTTPException(status_code=404, detail='Pokemon not found')
            db_trainer = session.query(Trainer).filter(Trainer.name == trainer_name).first()
            if db_trainer is None:
                raise HTTPException(status_code=404, detail='Trainer not found')
            else:
                trainer_pokemon = session.query(TrainerPokemon).filter(TrainerPokemon.pokemon_id == db_pokemon.id,
                                                                       TrainerPokemon.trainer_id == db_trainer.id).first()
                if trainer_pokemon:
                    raise HTTPException(status_code=409, detail='Trainer already owns this Pokemon')
            trainer_pokemon = TrainerPokemon(trainer_id=db_trainer.id, pokemon_id=db_pokemon.id)
            session.add(trainer_pokemon)
            session.commit()
            return f'Pokemon {pokemon_name} was successfully added to trainer {trainer_name}'

    def create_trainer(self, trainer_name: str, trainer_town: str):
        with self.session as session:
            db_trainer = session.query(Trainer).filter(Trainer.name == trainer_name).first()
            if db_trainer:
                raise HTTPException(status_code=409, detail='Trainer already exists')
            db_trainer = Trainer(name=trainer_name, town=trainer_town)
            session.add(db_trainer)
            session.commit()
            return f'Trainer {trainer_name} from {trainer_town} was successfully added to the database'

    def delete_trainer_by_name(self, trainer_name: str):
        with self.session as session:
            db_trainer = session.query(Trainer).filter(Trainer.name == trainer_name).first()
            if db_trainer is None:
                raise HTTPException(status_code=404, detail='Trainer not found')
            db_pokemons = session.query(TrainerPokemon).filter(TrainerPokemon.trainer_id == db_trainer.id).all()
            for db_pokemon in db_pokemons:
                session.delete(db_pokemon)
            session.delete(db_trainer)
            session.commit()
            return f'Trainer {trainer_name} was deleted successfully'
