import json
from database_connection import create_database_sql
from utils.api_operations import get_pokemon_details
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


def main():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    create_initial_trainers_database(config)
    edit_json_file(config)
    create_sql_database(config)
    create_mongo_database(config)


if __name__ == '__main__':
    main()
