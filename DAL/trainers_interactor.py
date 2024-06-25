from database_connection.database import session_local
from database_connection.models import Pokemon, Trainer, TrainerPokemon


class TrainersInteractor:
    def __init__(self):
        self.session = session_local()

    def close_session(self):
        self.session.close()

    def get_pokemon_by_name(self, pokemon_name):
        return self.session.query(Pokemon).filter(Pokemon.name == pokemon_name).first()

    def get_trainer_by_name(self, trainer_name):
        return self.session.query(Trainer).filter(Trainer.name == trainer_name).first()

    def delete_pokemon_of_trainer(self, pokemon_name, trainer_name):
        db_pokemon = self.get_pokemon_by_name(pokemon_name)
        if not db_pokemon:
            self.close_session()
            return 1

        db_trainer = self.get_trainer_by_name(trainer_name)
        if not db_trainer:
            self.close_session()
            return 2

        trainer_pokemon = self.session.query(TrainerPokemon).filter_by(trainer_id=db_trainer.id, pokemon_id=db_pokemon.id).first()
        if not trainer_pokemon:
            self.close_session()
            return 3

        self.session.delete(trainer_pokemon)
        self.session.commit()
        self.close_session()
        return f'Pokemon {pokemon_name} was successfully deleted from trainer {trainer_name}'

    def get_pokemon_trainers(self, pokemon_name):
        db_pokemon = self.get_pokemon_by_name(pokemon_name)
        if not db_pokemon:
            self.close_session()
            return None

        trainer_pokemons = self.session.query(TrainerPokemon).filter_by(pokemon_id=db_pokemon.id).all()
        trainers = [self.session.query(Trainer).get(tp.trainer_id).name for tp in trainer_pokemons]

        self.close_session()
        return trainers

    def add_pokemon_to_trainer(self, pokemon_name, trainer_name):
        db_pokemon = self.get_pokemon_by_name(pokemon_name)
        if not db_pokemon:
            self.close_session()
            return 1

        db_trainer = self.get_trainer_by_name(trainer_name)
        if not db_trainer:
            self.close_session()
            return 2

        trainer_pokemon = self.session.query(TrainerPokemon).filter_by(trainer_id=db_trainer.id, pokemon_id=db_pokemon.id).first()
        if trainer_pokemon:
            self.close_session()
            return 3  # Pokemon already assigned to this trainer

        trainer_pokemon = TrainerPokemon(trainer_id=db_trainer.id, pokemon_id=db_pokemon.id)
        self.session.add(trainer_pokemon)
        self.session.commit()
        self.close_session()
        return f'Pokemon {pokemon_name} was successfully added to trainer {trainer_name}'

    def create_trainer(self, trainer_name, trainer_town):
        if self.get_trainer_by_name(trainer_name):
            self.close_session()
            return None

        new_trainer = Trainer(name=trainer_name, town=trainer_town)
        self.session.add(new_trainer)
        self.session.commit()
        self.close_session()
        return f'Trainer {trainer_name} from {trainer_town} was successfully added to the database'

    def delete_trainer_by_name(self, trainer_name):
        db_trainer = self.get_trainer_by_name(trainer_name)
        if not db_trainer:
            self.close_session()
            return None

        # Delete all trainer's pokemons first
        trainer_pokemons = self.session.query(TrainerPokemon).filter_by(trainer_id=db_trainer.id).all()
        for tp in trainer_pokemons:
            self.session.delete(tp)

        self.session.delete(db_trainer)
        self.session.commit()
        self.close_session()
        return f'Trainer {trainer_name} was deleted successfully'
