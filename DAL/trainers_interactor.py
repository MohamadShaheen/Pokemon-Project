from database_connection.database import session_local
from database_connection.models import Pokemon, TrainerPokemon, Trainer


class TrainersInteractor:
    def __init__(self):
        self.session = session_local()

    def delete_pokemon_of_trainer(self, pokemon_name, trainer_name):
        db_pokemon = self.session.query(Pokemon).filter(Pokemon.name == pokemon_name).first()

        if db_pokemon is None:
            self.session.close()
            return 1

        db_trainer = self.session.query(Trainer).filter(Trainer.name == trainer_name).first()

        if db_trainer is None:
            self.session.close()
            return 2

        trainer_pokemon = self.session.query(TrainerPokemon).filter(TrainerPokemon.trainer_id == db_trainer.id,
                                                                    TrainerPokemon.pokemon_id == db_pokemon.id).first()
        if trainer_pokemon is None:
            self.session.close()
            return 3

        self.session.delete(trainer_pokemon)
        self.session.commit()
        self.session.close()

        return f'Pokemon {pokemon_name} was successfully deleted from trainer {trainer_name}'

    def get_pokemon_trainers(self, pokemon_name: str):
        db_pokemon = self.session.query(Pokemon).filter(Pokemon.name == pokemon_name).first()

        if db_pokemon is None:
            self.session.close()
            return None

        db_trainers = self.session.query(TrainerPokemon).filter(TrainerPokemon.pokemon_id == db_pokemon.id).all()
        trainers = []
        for item in db_trainers:
            db_trainer = self.session.query(Trainer).filter(Trainer.id == item.trainer.id).first()
            trainers.append(db_trainer.name)

        self.session.close()

        return trainers

    def add_pokemon_to_trainer(self, pokemon_name: str, trainer_name: str):
        db_pokemon = self.session.query(Pokemon).filter(Pokemon.name == pokemon_name).first()

        if db_pokemon is None:
            self.session.close()
            return 1

        db_trainer = self.session.query(Trainer).filter(Trainer.name == trainer_name).first()

        if db_trainer is None:
            self.session.close()
            return 2

        else:
            trainer_pokemon = self.session.query(TrainerPokemon).filter(TrainerPokemon.pokemon_id == db_pokemon.id,
                                                                        TrainerPokemon.trainer_id == db_trainer.id).first()
            if trainer_pokemon:
                self.session.close()
                return 3

        trainer_pokemon = TrainerPokemon(trainer_id=db_trainer.id, pokemon_id=db_pokemon.id)
        self.session.add(trainer_pokemon)
        self.session.commit()
        self.session.close()

        return f'Pokemon {pokemon_name} was successfully added to trainer {trainer_name}'

    def create_trainer(self, trainer_name: str, trainer_town: str):
        db_trainer = self.session.query(Trainer).filter(Trainer.name == trainer_name).first()

        if db_trainer:
            self.session.close()
            return None

        db_trainer = Trainer(name=trainer_name, town=trainer_town)
        self.session.add(db_trainer)
        self.session.commit()
        self.session.close()

        return f'Trainer {trainer_name} from {trainer_town} was successfully added to the database'

    def delete_trainer_by_name(self, trainer_name: str):
        db_trainer = self.session.query(Trainer).filter(Trainer.name == trainer_name).first()

        if db_trainer is None:
            self.session.close()
            return None

        db_pokemons = self.session.query(TrainerPokemon).filter(TrainerPokemon.trainer_id == db_trainer.id).all()
        for db_pokemon in db_pokemons:
            self.session.delete(db_pokemon)

        self.session.delete(db_trainer)
        self.session.commit()
        self.session.close()

        return f'Trainer {trainer_name} was deleted successfully'
