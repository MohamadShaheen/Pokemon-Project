import os
import json
import base64
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

host = os.getenv('MONGO_DATABASE_HOST')
port = os.getenv('MONGO_DATABASE_PORT')
database = os.getenv('MONGO_DATABASE_NAME')
collection = os.getenv('MONGO_DATABASE_COLLECTION')
trainers_collection = os.getenv('MONGO_TRAINERS_DATABASE_COLLECTION')
battle_collection = os.getenv('MONGO_BATTLE_DATABASE_COLLECTION')

mongo_database_url = f'mongodb://{host}:{port}/'
# mongo_database_url = f'mongodb://mongo:{port}/'


def create_database():
    client = MongoClient(mongo_database_url)
    my_database = client[database]
    my_collection = my_database[collection]

    with open('data/pokemons_data.json', 'r') as file:
        data = json.load(file)

    for entry in data:
        pokemon_id = entry['id']
        pokemon_name = entry['name']
        pokemon_image_url = entry['image_url']
        pokemon_image = base64.b64decode(entry['image_byte_array'])

        document = my_collection.find_one({'pokemon_name': pokemon_name})

        if document:
            if document['pokemon_image_url'] == pokemon_image_url:
                print(f'Image already stored in database as {pokemon_name}')
                continue

            my_collection.delete_one({'pokemon_name': pokemon_name})

        my_collection.insert_one({'_id': pokemon_id, 'pokemon_name': pokemon_name, 'pokemon_image_url': pokemon_image_url, 'pokemon_image': pokemon_image})
        print(f'The image of {pokemon_name} was successfully stored in the database!')


def create_trainers_database():
    client = MongoClient(mongo_database_url)
    my_database = client[database]
    my_collection = my_database[trainers_collection]

    with open('data/trainers_data.json', 'r') as file:
        data = json.load(file)

    for entry in data:
        trainer_name = entry['trainer_name']
        trainer_image_url = entry['trainer_image_url']
        trainer_image = base64.b64decode(entry['trainer_image'])

        document = my_collection.find_one({'trainer_name': trainer_name})

        if document:
            if document['trainer_image_url'] == trainer_image_url:
                print(f'Image already stored in database as {trainer_name}')
                continue

            my_collection.delete_one({'trainer_name': trainer_name})

        my_collection.insert_one(
            {'trainer_name': trainer_name, 'trainer_image_url': trainer_image_url,
             'trainer_image': trainer_image})
        print(f'The image of {trainer_name} was successfully stored in the database!')


def create_battle_database():
    client = MongoClient(mongo_database_url)
    my_database = client[database]
    my_collection = my_database[battle_collection]

    with open('data/pokemons_battle_data.json', 'r') as file:
        data = json.load(file)

    for entry in data:
        name = entry['name']

        document = my_collection.find_one({'pokemon_name': name})

        if document:
            if document['pokemon_name'] == name:
                print(f'Pokemon already stored in database as {name}')
                continue

            my_collection.delete_one({'pokemon_name': name})

        id = entry['id']
        moves = entry['moves']
        stats = entry['stats']

        moves_dict = {move[0]: {'power': move[1], 'type': move[2]} for move in moves}
        stats_dict = {stat[0]: stat[1] for stat in stats}

        my_collection.insert_one({'_id': id, 'pokemon_name': name, 'pokemon_moves': moves_dict, 'pokemon_stats': stats_dict})
