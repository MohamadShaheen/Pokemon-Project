import time

from DAL.images_interactor import ImagesInteractor
from DAL.pokemons_interactor import PokemonsInteractor
from DAL.trainers_interactor import TrainersInteractor
from database_connection.database import session_local
from database_connection.models import Trainer, Pokemon, TrainerPokemon
from utils.api_operations import get_evolved_pokemon


class EvolveInteractor:
    def __init__(self):
        self.session = session_local()

    def evolve_pokemon_of_trainer(self, pokemon_name: str, trainer_name: str):
        db_pokemon = self.session.query(Pokemon).filter(Pokemon.name == pokemon_name).first()

        if db_pokemon is None:
            self.session.close()
            return 1

        db_trainer = self.session.query(Trainer).filter(Trainer.name == trainer_name).first()

        if db_trainer is None:
            self.session.close()
            return 2

        db_trainer_pokemon = self.session.query(TrainerPokemon).filter(TrainerPokemon.trainer_id == db_trainer.id,
                                                                       TrainerPokemon.pokemon_id == db_pokemon.id).first()

        if db_trainer_pokemon is None:
            self.session.close()
            return 3

        evolved_pokemon = get_evolved_pokemon(pokemon_name=pokemon_name)
        if evolved_pokemon is None:
            return 4

        self.session.delete(db_trainer_pokemon)
        self.session.commit()
        self.session.close()

        pokemons_interactor = PokemonsInteractor()
        pokemons_interactor.add_new_pokemon(pokemon_name=evolved_pokemon)

        trainers_interactor = TrainersInteractor()
        trainers_interactor.add_pokemon_to_trainer(pokemon_name=evolved_pokemon, trainer_name=trainer_name)

        images_interactor = ImagesInteractor()
        images_interactor.show_image_by_name(pokemon_name=pokemon_name)
        time.sleep(0.1)
        images_interactor.insert_image(pokemon_name=evolved_pokemon)
        time.sleep(0.1)
        images_interactor.show_image_by_name(pokemon_name=evolved_pokemon)

        return f'Pokemon {pokemon_name} has been evolved to {evolved_pokemon} for trainer {trainer_name}'
