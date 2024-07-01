from datetime import datetime
import json
import os
import random
from dotenv import load_dotenv
from pymongo import MongoClient
from DAL.pokemons_interactor import PokemonsInteractor
from database_connection.create_database_mongo import mongo_database_url
from utils.api_operations import get_pokemon_battle_details

load_dotenv()

database = os.getenv('MONGO_DATABASE_NAME')
collection = os.getenv('MONGO_BATTLE_DATABASE_COLLECTION')


class BattleInteractor:
    def __init__(self):
        self.client = MongoClient(mongo_database_url)
        cursor = self.client[database]
        self.collection = cursor[collection]

    def _get_pokemon_moves_and_stats(self, pokemon_name: str):
        pokemon_details = self.collection.find_one({'pokemon_name': pokemon_name})
        pokemon_moves = pokemon_details['pokemon_moves']
        pokemon_stats = pokemon_details['pokemon_stats']

        return pokemon_moves, pokemon_stats

    @staticmethod
    def get_pokemon_detailed_stats(pokemon_stats):
        pokemon_hp = pokemon_stats['hp']
        pokemon_attack = pokemon_stats['attack']
        pokemon_defense = pokemon_stats['defense']
        pokemon_special_attack = pokemon_stats['special-attack']
        pokemon_special_defense = pokemon_stats['special-defense']

        return pokemon_hp, pokemon_attack, pokemon_defense, pokemon_special_attack, pokemon_special_defense

    @staticmethod
    def calculate_damage(attacker_attack, attacker_special_attack, defender_defense, defender_special_defense,
                         attacker_move_power, round_details):

        attack = random.choices([attacker_attack, attacker_special_attack], weights=[0.9, 0.1], k=1)[0]
        defense = random.choices([defender_defense, defender_special_defense], weights=[0.9, 0.1], k=1)[0]

        if attack == attacker_attack:
            round_details['Attack Type'] = 'Regular Attack'
        else:
            round_details['Attack Type'] = 'Special Attack'

        if defense == defender_defense:
            round_details['Defense Type'] = 'Regular Defense'
        else:
            round_details['Defense Type'] = 'Special Defense'

        if attacker_move_power is None:
            attacker_move_power = 0
        damage = (attack / defense) * attacker_move_power / 10
        damage *= random.uniform(0.85, 1.0)
        return int(damage)

    def simulate_battle(self, trainer1_name: str, pokemon1_name: str, trainer2_name: str, pokemon2_name: str):
        pokemons_interactor = PokemonsInteractor()
        trainer1_pokemons = pokemons_interactor.get_pokemons_by_trainer(trainer_name=trainer1_name)
        trainer2_pokemons = pokemons_interactor.get_pokemons_by_trainer(trainer_name=trainer2_name)

        if trainer1_pokemons is None:
            return 1

        if trainer2_pokemons is None:
            return 2

        if pokemon1_name not in trainer1_pokemons:
            return 3

        if pokemon2_name not in trainer2_pokemons:
            return 4

        pokemon1_moves, pokemon1_stats = self._get_pokemon_moves_and_stats(pokemon_name=pokemon1_name)
        pokemon2_moves, pokemon2_stats = self._get_pokemon_moves_and_stats(pokemon_name=pokemon2_name)

        pokemon1_hp, pokemon1_attack, pokemon1_defense, pokemon1_special_attack, pokemon1_special_defense = self.get_pokemon_detailed_stats(
            pokemon_stats=pokemon1_stats)
        pokemon2_hp, pokemon2_attack, pokemon2_defense, pokemon2_special_attack, pokemon2_special_defense = self.get_pokemon_detailed_stats(
            pokemon_stats=pokemon2_stats)

        battle_log = []

        turn = 0
        while pokemon1_hp > 0 and pokemon2_hp > 0:
            round_details = {}
            turn += 1
            round_details['Round'] = turn

            if turn % 2 == 1:
                attacker, defender = pokemon1_name, pokemon2_name
                move_name, move_details = random.choice(list(pokemon1_moves.items()))
                round_details[f'{trainer1_name} ({attacker}) Move'] = move_name
                damage = self.calculate_damage(pokemon1_attack, pokemon1_special_attack, pokemon2_defense,
                                               pokemon2_special_defense, move_details['power'], round_details)
                pokemon2_hp -= damage
                round_details['details'] = f'{defender} ({trainer2_name}) takes {damage} damage. Remaining HP: {pokemon2_hp}'
            else:
                attacker, defender = pokemon2_name, pokemon1_name
                move_name, move_details = random.choice(list(pokemon2_moves.items()))
                round_details[f'{trainer2_name} ({attacker}) Move'] = move_name
                damage = self.calculate_damage(pokemon2_attack, pokemon2_special_attack, pokemon1_defense,
                                               pokemon1_special_defense, move_details['power'], round_details)
                pokemon1_hp -= damage
                round_details['details'] = f'{defender} ({trainer1_name}) takes {damage} damage. Remaining HP: {pokemon1_hp}'

            battle_log.append(round_details)

        if pokemon1_hp <= 0:
            battle_log.append({
                                  'Battle Result': f'{pokemon1_name} ({trainer1_name}) fainted! {pokemon2_name} ({trainer2_name}) wins!'})
        else:
            battle_log.append({
                                  'Battle Result': f'{pokemon2_name} ({trainer2_name}) fainted! {pokemon1_name} ({trainer1_name}) wins!'})

        with open('data/detailed_battle_logs.json', 'r') as file:
            detailed_battle_logs = json.load(file)

        detailed_battle_logs.append({datetime.now().strftime("%d-%m-%Y %H:%M:%S"): battle_log})

        with open('data/detailed_battle_logs.json', 'w') as file:
            json.dump(detailed_battle_logs, file, indent=4)

        with open('data/brief_battle_logs.json', 'r') as file:
            brief_battle_logs = json.load(file)

        brief_battle_logs.append({datetime.now().strftime("%d-%m-%Y %H:%M:%S"): battle_log[-1]['Battle Result']})

        with open('data/brief_battle_logs.json', 'w') as file:
            json.dump(brief_battle_logs, file, indent=4)

        return battle_log

    def add_pokemon_battle_details(self, pokemon_name):
        if self.collection.find_one({'pokemon_name': pokemon_name}):
            return

        with open('data/existing_moves.json', 'r') as file:
            existing_moves = json.load(file)

        id, moves, stats = get_pokemon_battle_details(pokemon_name=pokemon_name, existing_moves=existing_moves)

        self.collection.insert_one({'_id': id, 'pokemon_name': pokemon_name, 'pokemon_moves': moves, 'pokemon_stats': stats})
