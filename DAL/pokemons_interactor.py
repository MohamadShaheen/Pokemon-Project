from utils.api_operations import get_pokemon_details
from database_connection.database import session_local
from database_connection.models import Pokemon, Type, TypePokemon, TrainerPokemon, Trainer


class PokemonsInteractor:
    def __init__(self):
        self.session = session_local()

    def get_pokemon_details_by_id(self, pokemon_id):
        db_pokemon = self.session.query(Pokemon).filter(Pokemon.id == pokemon_id).first()
        self.session.close()
        return db_pokemon

    def get_pokemon_details_by_name(self, pokemon_name: str):
        db_pokemon = self.session.query(Pokemon).filter(Pokemon.name == pokemon_name).first()
        self.session.close()
        return db_pokemon

    def get_pokemons_by_type(self, pokemon_type: str):
        db_type = self.session.query(Type).filter(Type.type == pokemon_type).first()

        if db_type is None:
            self.session.close()
            return None

        db_pokemons = self.session.query(TypePokemon).filter(TypePokemon.type_id == db_type.id).all()
        pokemons = []
        for item in db_pokemons:
            db_pokemon = self.session.query(Pokemon).filter(Pokemon.id == item.pokemon.id).first()
            pokemons.append(db_pokemon.name)

        self.session.close()

        return pokemons

    def get_pokemons_by_trainer(self, trainer_name: str):
        db_trainer = self.session.query(Trainer).filter(Trainer.name == trainer_name).first()

        if db_trainer is None:
            self.session.close()
            return None

        db_pokemons = self.session.query(TrainerPokemon).filter(TrainerPokemon.trainer_id == db_trainer.id).all()
        pokemons = []
        for item in db_pokemons:
            db_pokemon = self.session.query(Pokemon).filter(Pokemon.id == item.pokemon.id).first()
            pokemons.append(db_pokemon.name)

        self.session.close()

        return pokemons

    def add_new_pokemon(self, pokemon_name: str):
        db_pokemon = self.session.query(Pokemon).filter(Pokemon.name == pokemon_name).first()

        if db_pokemon:
            self.session.close()
            return 1

        types, height, weight, id, _ = get_pokemon_details(pokemon_name=pokemon_name)

        if types is None or height is None or weight is None:
            self.session.close()
            return 2

        db_pokemon = Pokemon(id=id, name=pokemon_name, height=height, weight=weight)
        self.session.add(db_pokemon)
        self.session.flush()

        for type in types:
            db_type = self.session.query(Type).filter(Type.type == type).first()
            if db_type is None:
                db_type = Type(type=type)
                self.session.add(db_type)
                self.session.flush()

            db_type_pokemon = TypePokemon(type_id=db_type.id, pokemon_id=db_pokemon.id)
            self.session.add(db_type_pokemon)
            self.session.flush()

        self.session.commit()
        self.session.close()

        return {'name': pokemon_name, 'height': height, 'weight': weight, 'types': types}

    def delete_pokemon_by_name(self, pokemon_name: str):
        db_pokemon = self.session.query(Pokemon).filter(Pokemon.name == pokemon_name).first()

        if db_pokemon is None:
            self.session.close()
            return None

        db_types = self.session.query(TypePokemon).filter(TypePokemon.pokemon_id == db_pokemon.id).all()
        for db_type in db_types:
            self.session.delete(db_type)

        db_trainers = self.session.query(TrainerPokemon).filter(TrainerPokemon.pokemon_id == db_pokemon.id).all()
        for db_trainer in db_trainers:
            self.session.delete(db_trainer)

        self.session.delete(db_pokemon)
        self.session.commit()
        self.session.close()

        return f'Pokemon {pokemon_name} was deleted successfully'
