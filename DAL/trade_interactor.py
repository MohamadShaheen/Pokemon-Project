import json
from datetime import datetime
from DAL.pokemons_interactor import PokemonsInteractor
from DAL.trainers_interactor import TrainersInteractor
from database_connection.database import session_local


class TradeInteractor:
    def __init__(self):
        self.session = session_local()

    def trade(self, trainer1_name: str, pokemon1_name: str, trainer2_name: str, pokemon2_name: str, trainer2_response: str):
        pokemons_interactor = PokemonsInteractor()
        trainer1_pokemons = pokemons_interactor.get_pokemons_by_trainer(trainer_name=trainer1_name)
        trainer2_pokemons = pokemons_interactor.get_pokemons_by_trainer(trainer_name=trainer2_name)

        if trainer1_pokemons is None:
            self.session.close()
            return 1

        if trainer2_pokemons is None:
            self.session.close()
            return 2

        if pokemon1_name not in trainer1_pokemons:
            self.session.close()
            return 3

        if pokemon2_name not in trainer2_pokemons:
            self.session.close()
            return 4

        if pokemon1_name in trainer2_pokemons:
            self.session.close()
            return 5

        if pokemon2_name in trainer1_pokemons:
            self.session.close()
            return 6

        response = trainer2_response.lower()
        acceptance_responses = {'1', 'yes', 'true', 't', 'y', 'yeah', 'accept', 'ok', 'bingo', 'alright', 'why not', 'fine', 'hla loya', 'agree', 'hundred percent'}
        rejection_responses = {'0', 'no', 'false', 'f', 'n', 'nope', 'reject', 'not okay', 'eww', 'not really', 'not fine', 'are you missed up', 'are you crazy', 'zero chance', 'disagree', 'are you out of your mind'}

        if response in acceptance_responses:
            trainers_interactor = TrainersInteractor()
            trainers_interactor.add_pokemon_to_trainer(pokemon_name=pokemon1_name, trainer_name=trainer2_name)
            trainers_interactor.add_pokemon_to_trainer(pokemon_name=pokemon2_name, trainer_name=trainer1_name)
            trainers_interactor.delete_pokemon_of_trainer(pokemon_name=pokemon1_name, trainer_name=trainer1_name)
            trainers_interactor.delete_pokemon_of_trainer(pokemon_name=pokemon2_name, trainer_name=trainer2_name)

            with open('data/trade_log.json', 'r') as file:
                trade_log = json.load(file)

            trade_log.append(f'{datetime.now().strftime("%d-%m-%Y %H:%M:%S")} - {trainer1_name} traded {pokemon1_name} with {trainer2_name} for {pokemon2_name}')
            with open('data/trade_log.json', 'w') as file:
                json.dump(trade_log, file, indent=4)

            return trade_log

        elif response in rejection_responses:
            self.session.close()
            return 7

        else:
            response = {
                'Acceptance Responses': acceptance_responses,
                'Rejection Responses': rejection_responses
            }

            return response
