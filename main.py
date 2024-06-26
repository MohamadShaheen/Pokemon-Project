import base64
import io
import json

from PIL import Image

from database_connection import create_database_sql
from utils.api_operations import get_pokemon_details, get_trainer_image_url
from database_connection import create_database_mongo
from utils.request_response_operations import get_base64_image_by_url


def edit_json_file(config):
    if config['database_editor'] == 0:
        with open('data/original_pokemons_data.json', 'r') as file:
            pokemon_data = json.load(file)

        for pokemon in pokemon_data:
            correct_types, _, _, id, image_url = get_pokemon_details(pokemon['name'])
            if correct_types:
                pokemon['types'] = correct_types
                if 'type' in pokemon:
                    del pokemon['type']

                pokemon['id'] = id
                pokemon['image_url'] = image_url
                pokemon['image_byte_array'] = get_base64_image_by_url(image_url=image_url)

        with open('data/pokemons_data.json', 'w') as file:
            json.dump(pokemon_data, file, indent=4)

        config['database_editor'] = 1
        with open('config.json', 'w') as config_file:
            json.dump(config, config_file, indent=4)
    else:
        print('JSON already up to date - check database_editor value in config.json file')


def create_initial_trainers_database(config):
    if config['create_initial_trainers_database'] == 1:
        print('Initial trainers database already created - Check create_initial_trainers_database value in config.json file')
        return

    trainers = []

    with open('data/original_pokemons_data.json', 'r') as file:
        data = json.load(file)

    for entry in data:
        for trainer in entry['ownedBy']:
            if trainer['name'] not in trainers:
                trainers.append(trainer['name'])

    with open('data/initial_trainers_data.json', 'w') as file:
        json.dump(trainers, file, indent=4)

    config['create_initial_trainers_database'] = 1
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)


def create_sql_database(config):
    if config['create_database_sql'] == 0:
        create_database_sql.create_database()

        config['create_database_sql'] = 1
        with open('config.json', 'w') as config_file:
            json.dump(config, config_file, indent=4)
    else:
        print('SQL database already created - check create_database_sql value in config.json file')


def create_mongo_database(config):
    if config['create_database_mongo'] == 0:
        create_database_mongo.create_database()

        config['create_database_mongo'] = 1
        with open('config.json', 'w') as config_file:
            json.dump(config, config_file, indent=4)
    else:
        print('Mongo database already created - check create_database_mongo value in config.json file')


def get_local_image_bytes():
    with Image.open('images/Anonymous.png') as image:
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format=image.format)
        trainer_image = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
        return trainer_image


def create_trainers_database(config):
    if config['create_trainers_database'] == 1:
        print('Trainers database already created - check create_trainers_database value in config.json file')
        return

    with open('data/initial_trainers_data.json', 'r') as file:
        data = json.load(file)

    trainers = []
    for trainer_name in data:
        print(trainer_name)
        if trainer_name == 'Lt. Surge':
            trainer_image_url = get_trainer_image_url(trainer_name='Surge')
            trainer_image = get_base64_image_by_url(image_url=trainer_image_url)

        elif trainer_name == 'Ash':
            trainer_image_url = 'https://archives.bulbagarden.net/media/upload/thumb/c/cd/Ash_JN.png/225px-Ash_JN.png'
            trainer_image = get_base64_image_by_url(image_url=trainer_image_url)

        elif trainer_name == 'Leaf':
            trainer_image_url = 'https://archives.bulbagarden.net/media/upload/thumb/4/48/FireRed_LeafGreen_Leaf.png/210px-FireRed_LeafGreen_Leaf.png'
            trainer_image = get_base64_image_by_url(image_url=trainer_image_url)

        elif trainer_name == 'Bane' or trainer_name == 'Genevive' or trainer_name == 'Brock' or trainer_name == 'Julia' or trainer_name == 'Loga':
            trainer_image_url = 'Not Available'
            trainer_image = get_local_image_bytes()

        else:
            trainer_image_url = get_trainer_image_url(trainer_name=trainer_name)
            trainer_image = get_base64_image_by_url(image_url=trainer_image_url)

        trainers.append({
            'trainer_name': trainer_name,
            'trainer_image_url': trainer_image_url,
            'trainer_image': trainer_image
        })

    config['create_trainers_database'] = 1
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)

    with open('data/trainers_data.json', 'w') as file:
        json.dump(trainers, file, indent=4)


def create_trainers_mongo_database(config):
    if config['create_trainers_database_mongo'] == 0:
        create_database_mongo.create_trainers_database()

        config['create_trainers_database_mongo'] = 1
        with open('config.json', 'w') as config_file:
            json.dump(config, config_file, indent=4)
    else:
        print('Trainers mongo database already created - check create_trainers_database_mongo value in config.json file')


def main():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    edit_json_file(config)
    create_sql_database(config)
    create_mongo_database(config)
    create_initial_trainers_database(config)
    create_trainers_database(config)
    create_trainers_mongo_database(config)


if __name__ == '__main__':
    main()
