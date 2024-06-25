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

#mongo_database_url = f'mongodb://{host}:{port}/'
mongo_database_url = f'mongodb://mongo:{port}/'


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
