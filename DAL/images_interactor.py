import base64
import os
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
from pymongo import MongoClient
from utils.api_operations import get_pokemon_details
from utils.request_response_operations import get_image_by_url
from database_connection.create_database_mongo import mongo_database_url

load_dotenv()

database = os.getenv('MONGO_DATABASE_NAME')
collection = os.getenv('MONGO_DATABASE_COLLECTION')
trainers_collection = os.getenv('MONGO_TRAINERS_DATABASE_COLLECTION')


class ImagesInteractor:
    def __init__(self):
        self.client = MongoClient(mongo_database_url)
        cursor = self.client[database]
        self.collection = cursor[collection]

    def get_image_by_id(self, pokemon_id):
        document = self.collection.find_one({'_id': pokemon_id})
        return document

    def get_image_by_name(self, pokemon_name):
        document = self.collection.find_one({'pokemon_name': pokemon_name})
        return document

    def get_trainer_image_by_name(self, trainer_name):
        collection = self.client[database][trainers_collection]
        document = collection.find_one({'trainer_name': trainer_name})
        return document

    def insert_image(self, pokemon_name):
        _, _, _, pokemon_id, pokemon_image_url = get_pokemon_details(pokemon_name=pokemon_name)

        document = self.collection.find_one({'pokemon_name': pokemon_name})

        if document:
            if document['pokemon_image_url'] == pokemon_image_url:
                return 'Pokemon already exists in the database'

            self.collection.delete_one({'pokemon_name': pokemon_name})

        pokemon_image = get_image_by_url(image_url=pokemon_image_url)

        self.collection.insert_one({'_id': pokemon_id, 'pokemon_name': pokemon_name, 'pokemon_image_url': pokemon_image_url, 'pokemon_image': pokemon_image})
        return None

    def delete_image(self, pokemon_name):
        document = self.collection.find_one({'pokemon_name': pokemon_name})

        if document is None:
            return f'Pokemon {pokemon_name} does not exist'

        self.collection.delete_one({'pokemon_name': pokemon_name})

    def show_image_by_name(self, pokemon_name):
        document = self.collection.find_one({'pokemon_name': pokemon_name})

        if document:
            image_byte_array = document['pokemon_image']
            image = Image.open(BytesIO(image_byte_array))
            image.show()
        else:
            return f'Pokemon {pokemon_name} does not exist'

    def show_image_by_id(self, pokemon_id):
        document = self.collection.find_one({'_id': pokemon_id})

        if document:
            image_byte_array = document['pokemon_image']
            image = Image.open(BytesIO(image_byte_array))
            image.show()
        else:
            return f'Pokemon with ID {pokemon_id} does not exist'

    def edit_image(self, pokemon_name, new_pokemon_image_url):
        document = self.collection.find_one({'pokemon_name': pokemon_name})

        if document is None:
            return f'Pokemon {pokemon_name} does not exist'

        if document['pokemon_image_url'] == new_pokemon_image_url:
            return 'You are providing the same existing pokemon image'

        response = get_image_by_url(image_url=new_pokemon_image_url)

        if response is None:
            return f'You are trying to insert invalid image. Please check the URL that you provided'

        self.collection.update_one({'pokemon_name': pokemon_name}, {'$set': {'pokemon_image_url': new_pokemon_image_url, 'pokemon_image': response}})
