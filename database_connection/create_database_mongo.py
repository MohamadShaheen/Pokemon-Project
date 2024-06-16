import os
import json
from dotenv import load_dotenv
from pymongo import MongoClient
from utils.api_operations import get_pokemon_image
from utils.request_response_operations import get_image_by_url

load_dotenv()

host = os.getenv('MONGO_DATABASE_HOST')
port = os.getenv('MONGO_DATABASE_PORT')
database = os.getenv('MONGO_DATABASE_NAME')
collection = os.getenv('MONGO_DATABASE_COLLECTION')


def create_database():
    # client = MongoClient(f'mongodb://{host}:{port}/')
    client = MongoClient(f'mongodb://mongo:{port}/')
    my_database = client[database]
    my_collection = my_database[collection]

    with open('data/pokemons_data.json', 'r') as file:
        data = json.load(file)

    for entry in data:
        pokemon_name = entry['name']
        pokemon_id, pokemon_image_url = get_pokemon_image(pokemon_name=pokemon_name)
        pokemon_image = get_image_by_url(image_url=pokemon_image_url)

        document = my_collection.find_one({'pokemon_name': pokemon_name})

        if document:
            if document['pokemon_image'] == pokemon_image:
                print(f'Image already stored in database as {pokemon_name}')
                continue

            my_collection.delete_one({'pokemon_name': pokemon_name})

        my_collection.insert_one({'_id': pokemon_id, 'pokemon_name': pokemon_name, 'pokemon_image_url': pokemon_image_url, 'pokemon_image': pokemon_image})
        print(f'The image of {pokemon_name} was successfully stored in the database!')
